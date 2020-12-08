/***************************************************************************
 *                                  _   _ ____  _
 *  Project                     ___| | | |  _ \| |
 *                             / __| | | | |_) | |
 *                            | (__| |_| |  _ <| |___
 *                             \___|\___/|_| \_\_____|
 *
 * Copyright (C) 1998 - 2017, Daniel Stenberg, <daniel@haxx.se>, et al.
 *
 * This software is licensed as described in the file COPYING, which
 * you should have received as part of this distribution. The terms
 * are also available at https://curl.haxx.se/docs/copyright.html.
 *
 * You may opt to use, copy, modify, merge, publish, distribute and/or sell
 * copies of the Software, and permit persons to whom the Software is
 * furnished to do so, under the terms of the COPYING file.
 *
 * This software is distributed on an "AS IS" basis, WITHOUT WARRANTY OF ANY
 * KIND, either express or implied.
 *
 ***************************************************************************/
/* <DESC>
 * Issue an HTTP POST and provide the data through the read callback.
 * </DESC>
 */
#include <stdio.h>
#include <string.h>
#include <curl/curl.h>

#include <string>
#include <iostream>
#include <fstream>
#include <list>
#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;


#undef USE_CHUNKED

/* silly test data to POST */
/*
static const char data[]="Lorem ipsum dolor sit amet, consectetur adipiscing "
"elit. Sed vel urna neque. Ut quis leo metus. Quisque eleifend, ex at "
"laoreet rhoncus, odio ipsum semper metus, at tempus ante urna in mauris. "
"Suspendisse ornare tempor venenatis. Ut dui neque, pellentesque a varius "
"eget, mattis vitae ligula. Fusce ut pharetra est. Ut ullamcorper mi ac "
"sollicitudin semper. Praesent sit amet tellus varius, posuere nulla non, "
"rhoncus ipsum.";
*/

struct WriteThis {
    const char *readptr;
    size_t sizeleft;
};

static size_t read_callback(void *dest, size_t size, size_t nmemb, void *userp) {
    struct WriteThis *wt = (struct WriteThis *)userp;
    size_t buffer_size = size*nmemb;

    if(wt->sizeleft) {
        /* copy as much as possible from the source to the destination */
        size_t copy_this_much = wt->sizeleft;

        if(copy_this_much > buffer_size) {
            copy_this_much = buffer_size;
        }
        memcpy(dest, wt->readptr, copy_this_much);

        wt->readptr += copy_this_much;
        wt->sizeleft -= copy_this_much;
        return copy_this_much; /* we copied this many bytes */
    }

    return 0; /* no more data left to deliver */
}

size_t write_callback(void *buffer, size_t size, size_t nmemb, void *userp) {
   return size * nmemb;
}

const list<string> onList = {"on","ON","true","TRUE", "yes","YES" };

int main(int argc, char *argv[]) {
    CURL *curl;
    CURLcode res;
    struct curl_slist *list = NULL;

    string token;
    struct WriteThis wt;

    if(argc != 3) {
        cout << "Usage: restSet <entity_id> <value>" << endl;
        exit(1);
    }

    string entity_id = argv[1];
    string value = argv[2];

    ifstream myfile ("haToken.txt");
    if (myfile.is_open()) {
        getline (myfile,token);

        myfile.close();
    } else { 
        cout << "Unable to open file" << endl << endl;
        exit(1);
    }   

    string payload = "{\"entity_id\": \"" + entity_id + "\"}";
    wt.readptr = payload.c_str();
    wt.sizeleft = payload.length();

    /* In windows, this will init the winsock stuff */
    res = curl_global_init(CURL_GLOBAL_DEFAULT);
    /* Check for errors */
    if(res != CURLE_OK) {
        fprintf(stderr, "curl_global_init() failed: %s\n", curl_easy_strerror(res));
        return 1;
    }

    /* get a curl handle */
    curl = curl_easy_init();
    if(curl) {

        string url = "http://192.168.10.124:8123/api/services/switch/";

        int n=count(onList.begin(), onList.end(), value);

        if ( n != 0) {
            url += "turn_on";
        } else {
            url += "turn_off";
        }

        /* First set the URL that is about to receive our POST. */
        curl_easy_setopt(curl, CURLOPT_URL,url.c_str());

        /* Now specify we want to POST data */
        curl_easy_setopt(curl, CURLOPT_POST, 1L);

        /* we want to use our own read function */
        curl_easy_setopt(curl, CURLOPT_READFUNCTION, read_callback);

        /* pointer to pass to our read function */
        curl_easy_setopt(curl, CURLOPT_READDATA, &wt);

        /* get verbose debug output please */
//        curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
        curl_easy_setopt(curl, CURLOPT_VERBOSE, 0L);

        string tmp = "Authorization: Bearer " + token ;

        list = curl_slist_append(list, "content-type: application/json/");
        list = curl_slist_append(list, tmp.c_str() );
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);

        /*
           If you use POST to a HTTP 1.1 server, you can send data without knowing
           the size before starting the POST if you use chunked encoding. You
           enable this by adding a header like "Transfer-Encoding: chunked" with
           CURLOPT_HTTPHEADER. With HTTP 1.0 or without chunked transfer, you must
           specify the size in the request.
           */
#ifdef USE_CHUNKED
        {
            struct curl_slist *chunk = NULL;

            chunk = curl_slist_append(chunk, "Transfer-Encoding: chunked");
            res = curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
            /* use curl_slist_free_all() after the *perform() call to free this
               list again */
        }
#else
        /* Set the expected POST size. If you want to POST large amounts of data,
           consider CURLOPT_POSTFIELDSIZE_LARGE */
        curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, (long)wt.sizeleft);
#endif

#ifdef DISABLE_EXPECT
        /*
           Using POST with HTTP 1.1 implies the use of a "Expect: 100-continue"
           header.  You can disable this header with CURLOPT_HTTPHEADER as usual.
NOTE: if you want chunked transfer too, you need to combine these two
since you can only set one list of headers with CURLOPT_HTTPHEADER. */

        /* A less good option would be to enforce HTTP 1.0, but that might also
           have other implications. */
        {
            struct curl_slist *chunk = NULL;

            chunk = curl_slist_append(chunk, "Expect:");
            res = curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
            /* use curl_slist_free_all() after the *perform() call to free this
               list again */
        }
#endif

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        /* Perform the request, res will get the return code */
        res = curl_easy_perform(curl);
        /* Check for errors */
        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

        /* always cleanup */
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
    return 0;
}
