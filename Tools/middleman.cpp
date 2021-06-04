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

#include <poll.h>

#include <string>

#include <iostream>
#include <fstream>
#include <list>
#include <algorithm>
#include <nlohmann/json.hpp>

#include "mqttHelper.h"

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

std::string ltrim(const std::string &s, const string WHITESPACE) {
    size_t start = s.find_first_not_of(WHITESPACE);
    return (start == std::string::npos) ? "" : s.substr(start);
}

std::string rtrim(const std::string &s, const string WHITESPACE) {
    size_t end = s.find_last_not_of(WHITESPACE);
    return (end == std::string::npos) ? "" : s.substr(0, end + 1);
}

std::string trim(const std::string &s, const string WHITESPACE) {
    return rtrim(ltrim(s, WHITESPACE),WHITESPACE);
}

size_t write_callback(void *buffer, size_t size, size_t nmemb, void *userp) {
    return size * nmemb;
}

const list<string> onList = {"on","ON","true","TRUE", "yes","YES" };
const list<string> offList = {"off","OFF","false","FALSE", "no","NO" };

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

    fd_set rd;
    struct timeval tv;
    int ret;

    if(buffer == NULL || size == 0)
        return false;

    //    while(read(STDIN_FILENO, &c, 1) == 1 && cnt < size - 1) {
    while(1) {
        tv.tv_sec  = 0;
        tv.tv_usec = 500000; // 500 ms

        FD_ZERO(&rd);
        FD_SET(STDIN_FILENO, &rd);

        ret = select(STDIN_FILENO + 1, &rd, NULL, NULL, &tv);

        if( ret > 0) {
            read(STDIN_FILENO, &c, 1);
            if(c == '\n') {
                buffer[cnt] = 0;
                return true;
            } else {
                buffer[cnt++] = c;
            }
        }

        if ( ret == 0) {
            cout << "Timeout" << endl;
        }
//        buffer[cnt++] = c;
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
    cout << "-OK" << endl;
    return true;
}

void doGet(string entity_id) {
    CURL *curl;
    CURLcode res;
    struct curl_slist *list = NULL;

    bool logical=false;
    string prefix = "switch";
    string subData = "[";

    char *more;
    string path;

    char element[64];
    char *elementName;

    more = strchr( (char *)entity_id.c_str(), '[');

    if(entity_id.substr(0,prefix.size()) == prefix) {
        logical = true;
        path = "";
    } else if (more != NULL ) {
        path = trim(more, "[]");
        cout << path << endl;

        strcpy( element, entity_id.c_str());

        char *tmp = strtok(element,"[]");
        char *tmp1 = strtok(NULL,"[]");

        cout << tmp << endl;
        cout << tmp1 << endl;

        entity_id = tmp;
        elementName = tmp1;

    }

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

        json inJson;

        inJson = json::parse( chunk.memory );

        if ( inJson["message"] == "Entity not found.") {
            cout << "-ERROR" << endl;
        }  else {

            string state = inJson["state"];

            state.erase(remove( state.begin(), state.end(), '\"' ),state.end());

            string out = "+GET " + entity_id + " ";

            if (logical) {
                if ( count(onList.begin(), onList.end(), state) != 0) {
                    out += "ON";
                } else if ( count(offList.begin(), offList.end(), state) != 0) {
                    out += "OFF";
                } else { 
                    out += state;
                }
                cout << out << endl;
            } else {
                string tmp = trim(state,string(" \n\r\t\f\v"));
                cout << out + tmp ;
                //                cout << chunk.memory << endl;
                cout << path << endl;
            }
        }
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

            if(line[0] == '^' ) {
                if(!strcmp(line,"^EXIT")) {
                    printf("EXIT\n");
                    run = false;
                } else if (!strcmp(line,"^HELP")) {
                    printf("HELP\n");
                } else if (!strcmp(line,"^PING")) {
                    printf("PONG\n");
                } else {
                    int tokCount = 1;

                    char buffer[100];

                    strcpy(buffer,line);

                    tok[0] = strtok(buffer," ");

                    tok[1] = strtok(NULL," ");
                    if(tok[1] != NULL) {
                        tokCount++;
                        tok[2] = strtok(NULL," ");
                        if(tok[2] != NULL) {

                            tokCount++;
                        }
                    }
                    bool fail = parseCmd(tokCount, tok);
                    if(fail) {
                        printf("-ERROR\n");
                    }
                }

            } else {
                printf("-ERROR\n");
            }

        } else {
            fprintf(stderr,"Read failed\n");
        }
    }
}


