/***************************************************************************
 *                                  _   _ ____  _
 *  Project                     ___| | | |  _ \| |
 *                             / __| | | | |_) | |
 *                            | (__| |_| |  _ <| |___
 *                             \___|\___/|_| \_\_____|
 *
 * Copyright (C) 1998 - 2018, Daniel Stenberg, <daniel@haxx.se>, et al.
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
 * Very simple HTTP GET
 * </DESC>
 */
#include <stdio.h>
#include <curl/curl.h>
#include <string>

#include <iostream>
#include <fstream>

using namespace std;

int main(void) {
    CURL *curl;
    CURLcode res;
    struct curl_slist *list = NULL;

    string token;
    ifstream myfile ("haToken.txt");
    if (myfile.is_open()) {
        getline (myfile,token);

        myfile.close();
    } else { 
        cout << "Unable to open file" << endl << endl;
        exit(1);
    }

    curl = curl_easy_init();

    if(curl) {
        string tmp = "Authorization: Bearer " + token ;
        cout << ">" << tmp << "<" << endl;
        list = curl_slist_append(list, "content-type: application/json/");
        list = curl_slist_append(list, tmp.c_str() );

        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);

        curl_easy_setopt(curl, CURLOPT_URL, "http://192.168.10.124:8123/api/states");
        /* example.com is redirected, so we tell libcurl to follow redirection */
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

        /* Perform the request, res will get the return code */
        res = curl_easy_perform(curl);
        /* Check for errors */
        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));

        /* always cleanup */
        curl_easy_cleanup(curl);
    }
    return 0;
}
