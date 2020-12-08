#include <stdio.h>
#include <curl/curl.h>
#include <string>

#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;

struct MemoryStruct {
  char *memory;
  size_t size;
};

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


int main(int argc, char *argv[]) {
    CURL *curl;
    CURLcode res;
    struct curl_slist *list = NULL;

    string token;
    struct MemoryStruct chunk;

    if(argc != 2) {
        cout << "Usage: restGet <entity_id>" << endl;
        exit(1);
    }

    string entity_id = argv[1];

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
//        curl_easy_setopt(curl, CURLOPT_URL, "http://192.168.10.124:8123/api/states");
        /* example.com is redirected, so we tell libcurl to follow redirection */
//        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

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

//        cout << "State is " + state << endl;
        cout << state << endl;


    }
    return 0;
}
