Goal -- what is the divorce rate of hollywood actors

Todo
* key takeaways and other discussions, wrap up
* make it reproducible
* re-put in charts
* after that if time, can look at some of these other questions
* maybe go back and make taco bell reproducible

* we want to take this and get 
    * number of marriages
    * number of actors who have been married N times
    * number of actors who have been divorced N times
    * marriage failure rate
        * overall, 1st, 2nd, n times 

    * go back and stick in the never marrieds

    * lengths of marriages
    
    * pct of actors divorced
    * what % of actors contribute what % of divorces

    * general QA
    * do we need to de-dupe for the same relationships? e.g. jen married to brad pitt, divorce counts for both of them are we then double counting? Can think about, worth addressing, idk if worth it to do the de-duping
    * see quickly about getting length of marriages, is there a cutoff that predicts survival
    * divorce probability over # of years of marriage
    



    
* QA Notes
    * we lose 11 actors and the spouses going from list of dicts to df, because our regex doesn't handle them properly (no parenthesis, just names), and handling them properly breaks other people.
    * 134 actors show up as never married, and we don't have them in the data at the moment

    * some clear things to check
        * number of people who have nan first event but don't have partners (this is an error) -- cleaned most of the different ways this can arise
        * check the never people
            * check that those who don't appear in the df indeed don't have spouses
                * step through for a handful and see why this is the case -- whoopi goldberg, client eastwood
            * 
        * check how many were unscrapable/only pulled url data -- e.g. kevin harts

    * how many don't have dates
    * make sure the df is sorted chronologically when running the window function, so that first marriages are showing up first/survs are showing up last


Done
* grab the info boxes

backlog
process the spouses, then the spouse, then the spouse(s) column
dig deeper on the regex of the first and the second events, modify a bit to the check both the first and second event numbers 
Will need to pull the 1000 actors list or find a new one


To Note
'\u200b' gpt wasn't great about the parsing. The whole thing of trying to use it to parse semi messy things, it wasn't as good as me trying myself. But couldn't know that til we tried it
Some interesting things about how much to give gpt and how to do yourself -- outsourcing a lot of hte thinking to the AI 
Some thoughts about obsessing over data quality
Intelligent use of AI -- ran out of API calls quickly

Future
grab the personal life section and use LLMs over it

References:
https://pypi.org/project/Wikipedia-API/
https://platform.openai.com/usage/activity