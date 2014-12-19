//
//  main.c
//  search
//
//  Created by Conor Taylor on 28/01/2014.
//  Copyright (c) 2014 Conor Taylor. All rights reserved.
//

#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

struct match {
    int loc;
    char *str;
};

char *nextSpace(char *str) {
    while (*str != '\0') {
        if (isspace(*str))
            return str;
        str++;
    }
    return str;
}

void cleanStr(char *str) {
    while (*str != '\0') {
        if (*str == '\n')
            *str = ' ';
        str++;
    }
}

struct match *search(char *schstr, char *schseq) {
    int maxMatches = 5, matchCount = 0;
    struct match *matches = malloc(sizeof(struct match)*maxMatches);
    char *strptr = schstr, *seqptr = schseq;
    int loc = -1;
    
    const char *invalid_characters = "().,></\\";
    int space = 1, ignore = 0;
    
    while (*strptr != '\0') {
        // reset for whitespace characters
        if (isspace(*strptr))
            space = 1;
        // ignore items in brackets
        else if (*strptr == '(' || *strptr == ')')
            ignore = !ignore;
        // process first item after space
        else if (space && !ignore) {
            space = 0;
            // make sure it's a valid character
            if (!strchr(invalid_characters, *strptr)) {
                // check against search sequence
                if (tolower(*strptr) == *seqptr) {
                    if (loc == -1)
                        loc = (int)(strptr-schstr);
                    seqptr++;
                    
                    // match found
                    if (*seqptr == '\0') {
                        struct match newMatch;
                        newMatch.loc = loc;
                        
                        long matchLen = (nextSpace(strptr)-(schstr+loc));
                        newMatch.str = malloc(sizeof(char)*(matchLen+1));
                        
                        memcpy(newMatch.str, schstr+loc, matchLen);
                        *(newMatch.str+matchLen) = '\0';
                        cleanStr(newMatch.str);
                        
                        if (maxMatches <= matchCount) {
                            maxMatches += 5;
                            realloc(matches, maxMatches);
                        }
                        *(matches+matchCount) = newMatch;
                        matchCount++;
                        
                        printf("MATCH: loc = %i, \"%s\"\n", newMatch.loc, newMatch.str);
                        seqptr = schseq;
                    }
                }
                else {
                    loc = -1;
                    seqptr = schseq;
                }
            }
        }
        strptr++;
    }
    return matches;
}

int main(int argc, const char * argv[]) {
    char *file_contents;
    long input_file_size;
    FILE *input_file = fopen("/Users/Conor/Documents/Lyrics/code/test.txt", "rb");
    fseek(input_file, 0, SEEK_END);
    input_file_size = ftell(input_file);
    rewind(input_file);
    file_contents = malloc((input_file_size + 1)*sizeof(char));
    fread(file_contents, sizeof(char), input_file_size, input_file);
    fclose(input_file);
    file_contents[input_file_size] = 0;
    
    struct match *matches;
    matches = search(file_contents, "ctrnom");
}