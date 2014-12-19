#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

struct string {
	char *ptr;
	size_t len;
};

void init_string(struct string *s) {
	s->len = 0;
	s->ptr = malloc(s->len+1);
	if (s->ptr == NULL) {
		fprintf(stderr, "malloc() failed\n");
		exit(EXIT_FAILURE);
	}
	s->ptr[0] = '\0';
}

size_t writefunc(void *ptr, size_t size, size_t nmemb, struct string *s) {
	size_t new_len = s->len + size*nmemb;
	s->ptr = realloc(s->ptr, new_len+1);
	if (s->ptr == NULL) {
		fprintf(stderr, "realloc() failed\n");
		exit(EXIT_FAILURE);
	}
	memcpy(s->ptr+s->len, ptr, size*nmemb);
	s->ptr[new_len] = '\0';
	s->len = new_len;

	return size*nmemb;
}

void parseToTree(char *s, char *t) {
	//char *tag = malloc)(sizeof(char)*2);
	char *tag; //temp
	*tag = '<';
	*(tag+1) = strdup(t);
	*(tag+strlen(t)+1) = '>';
	printf("tag = %s/n", tag);
}

int main(void) {
	CURL *curl;
	CURLcode res;

	curl = curl_easy_init();
	if(curl) {
		struct string s;
		init_string(&s);

		curl_easy_setopt(curl, CURLOPT_URL, "http://lyrics.wikia.com/api.php?action=lyrics&artist=Beatles&fmt=xml&func=getSong");
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writefunc);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, &s);
		res = curl_easy_perform(curl);

		printf("%s\n", s.ptr);
		//parseToTree(s.ptr, "item");
		free(s.ptr);

		/* always cleanup */
		curl_easy_cleanup(curl);
	}
	return 0;
}
