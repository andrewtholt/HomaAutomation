#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

#include <stdbool.h>
#include <unistd.h>
#include <ctype.h>

#include <sys/types.h>
#include <sys/stat.h>

#include <string>

#include <iostream>
#include <fstream>
#include <list>
#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;


#undef USE_CHUNKED

#define STDIN_FILENO 0

struct WriteThis {
    const char *readptr;
    size_t sizeleft;
};

struct MemoryStruct {
    char *memory;
    size_t size;
};

size_t write_callback(void *buffer, size_t size, size_t nmemb, void *userp) {
    return size * nmemb;
}

const list<string> onList = {"on","ON","true","TRUE", "yes","YES" };

static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;

    //  char *ptr = (char *)realloc(mem->memory, mem->size + realsize + 1);
    char *ptr = (char *)realloc(mem->memory, realsize + 1);
    if(ptr == NULL) {
        /* out of memory! */
        printf("not enough memory (realloc returned NULL)\n");
        return 0;
    }

    mem->memory = ptr;
    //  memcpy(&(mem->memory[mem->size]), contents, realsize);
    memcpy(mem->memory, contents, realsize);
    mem->size = realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}
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

char *trimWhiteSpace(char *str) {
    char *end;

    // Trim leading space
    while(isspace((unsigned char)*str)) str++;

    if(*str == 0)  // All spaces?
        return str;

    // Trim trailing space
    end = str + strlen(str) - 1;
    while(end > str && isspace((unsigned char)*end)) end--;

    // Write new null terminator character
    end[1] = '\0';

    return str;
}

bool getFromIn(char *buffer, size_t size) {
    size_t cnt = 0;
    char c;

    if(buffer == NULL || size == 0)
        return false;

    while(read(STDIN_FILENO, &c, 1) == 1 && cnt < size - 1) {
        if(c == '\n') {
            buffer[cnt] = 0;
            return true;
        }

        buffer[cnt++] = c;
    }

    buffer[cnt] = 0; // making sure it's 0-terminated
    return true;
}

bool doSet(string entity_id, string value) {
    CURL *curl;
    CURLcode res;
    struct curl_slist *list = NULL;

    bool fail=true;
    struct WriteThis wt;

    FILE *tokenFile;
    string token;

    //    cerr << "set " + entity_id + " to " << value << endl;

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

    res = curl_global_init(CURL_GLOBAL_DEFAULT);
    if(res != CURLE_OK) {
        fprintf(stderr, "curl_global_init() failed: %s\n", curl_easy_strerror(res));

        fail = true;

        return fail;
    }

    curl = curl_easy_init();
    if(curl) {
        string url = "http://192.168.10.124:8123/api/services/switch/" ;

        int n=count(onList.begin(), onList.end(), value);

        if( n != 0) {
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

        string tmp= "Authorization: Bearer " + token ;

        list = curl_slist_append(list, "content-type: application/json/");
        list = curl_slist_append(list, tmp.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
#ifdef USE_CHUNKED
        {
            struct curl_slist *chunk = NULL;

            //            chunk = curl_slist_append(chunk, "Transfer-Encoding: chunked");
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
#warning DISABLE_EXPECT
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
}

string doGet(string entity_id) {
    //    cout << "get " <<  entity_id;

    CURL *curl;
    CURLcode res;
    struct curl_slist *list = NULL;

    struct MemoryStruct chunk;

    string token;


    memset((void *)&chunk, 0, sizeof chunk);

    bool fail=true;

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
        string url = "http://192.168.10.124:8123/api/states/" + entity_id;

        string tmp = "Authorization: Bearer " + token ;
        //        cout << ">" << tmp << "<" << endl;
        list = curl_slist_append(list, "content-type: application/json/");
        list = curl_slist_append(list, tmp.c_str() );

        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

        /* Perform the request, res will get the return code */
        res = curl_easy_perform(curl);
        /* Check for errors */
        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));

        /* always cleanup */
        curl_easy_cleanup(curl);

        //        printf("%s\n", chunk.memory);

        json inJson;

        inJson = json::parse( chunk.memory );

        string state = inJson["state"];

        state.erase(remove( state.begin(), state.end(), '\"' ),state.end());

        cout << state << endl;

    }
}

char *doSub(char *entity_id) {
    printf("sub to %s \n", entity_id);
}

bool parseCmd(int count, char *tokens[3]) {
    bool fail=true;
    char buffer[1000];

    switch(count) {
        case 1:
            printf("One\n");
            break;
        case 2:
            if (!strcmp("^GET", tokens[0])) {
                doGet(tokens[1]);
                fail = false;
            } else if (!strcmp("^SUB", tokens[0])) {
                doSub(tokens[1]);
                fail = false;
            }
            break;
        case 3:
            if (!strcmp("^SET", tokens[0])) {
                doSet(tokens[1],tokens[2]);
                fail = false;
            }
            break;
        default:
            break;
    }
    return fail;
}

int main() {

    bool run=true;

    char line[100];

    bool OK=false;


    char *tok[3];
    while( run ) {
        OK = getFromIn(line,sizeof line);
        if(OK) {
            trimWhiteSpace(line);
            //            fprintf(stderr,"=>%s\n", line);

            if(line[0] == '^' ) {
                if(!strcmp(line,"^EXIT")) {
                    printf("EXIT\n");
                    run = false;
                } else if (!strcmp(line,"^PING")) {
                    printf("PONG\n");
                } else {
                    int tokCount = 1;

                    char buffer[100];

                    strcpy(buffer,line);

                    tok[0] = strtok(buffer," ");
                    //                    printf("tok[0] is %s\n", tok[0]);

                    tok[1] = strtok(NULL," ");
                    if(tok[1] != NULL) {
                        tokCount++;
                        //                        printf("tok[1] is %s\n", tok[1]);
                        tok[2] = strtok(NULL," ");
                        if(tok[2] != NULL) {
                            //                            printf("tok[2] is %s\n", tok[2]);
                            tokCount++;
                        }
                    }
                    bool fail = parseCmd(tokCount, tok);
                    if(fail) {
                        printf("^ERROR\n");
                    }
//                    printf("Tok count %d\n",tokCount);
                }

            } else {
                printf("ERROR\n");
            }

        } else {
            fprintf(stderr,"Read failed\n");
        }
    }
}


