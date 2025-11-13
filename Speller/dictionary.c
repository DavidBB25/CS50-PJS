// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// global var to keep track of words on dictionary
int dictwords = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO

    // hash word
    int array = hash(word);

    // check if word is in the hash table
    node *n = table[array];
    while (n != NULL)
    {
        // if is word
        if (strcasecmp(n->word, word) == 0)
        {
            return true;
        }

        // if is not word
        n = n->next;
    }
    // if next is null
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function

    // Handle empty string or non-alphabetic start
    if (word == NULL || word[0] == '\0' || !isalpha(word[0]))
    {
        return 0;
    }
    // Assuming N=26 for simple alphabetic hash
    return (toupper(word[0]) - 'A') % N; // Modulo N ensures it's within bounds [0, N-1]
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO

    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Failed to open dictionary.\n");
        fclose(file);
        return false;
    }

    // Read strings from file
    while (true)
    {
        char word[LENGTH + 1];
        int success = fscanf(file, "%s", word);
        if (success == EOF)
        {
            break;
        }

        // Create a new node for each word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Failed to allocate memory to a word\n");
            return false;
        }
        n->next = NULL;
        strcpy(n->word, word);

        // hash word
        int array = hash(n->word);

        // insert node into hash table
        if (table[array] == NULL)
        {
            table[array] = n;
        }
        else
        {
            n->next = table[array];
            table[array] = n;
        }
        dictwords++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return dictwords;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO

    for (int i = 0; i < N; i++)
    {
        node *n = table[i];
        node *tmp = NULL;
        while (n != NULL)
        {
            tmp = n;
            n = n->next;
            free(tmp);
        }
        table[i] = NULL;
    }
    return true;
}
