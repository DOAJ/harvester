ARTICLE_SOURCE = {
    "bibjson" : {
        "title" : "Article Title",
        "identifier": [
            {"type" : "doi", "id" : "10.0000/SOME.IDENTIFIER"},
            {"type": "pissn", "id": "1874-396X"}
        ],
        "journal" : {
            "volume" : "1",
            "number" : "99",
            "publisher" : "The Publisher",
            "title" : "The Title",
            "license" : [
                {
                    "title" : "CC BY",
                    "type" : "CC BY",
                    "url" : "http://license.example.com",
                    "version" : "1.0",
                    "open_access": True,
                }
            ],
            "language" : ["EN", "FR"],
            "country" : "US"
        },
        "year" : "1991",
        "month" : "January",
        "start_page" : "3",
        "end_page" : "21",
        "link" : [
            {
                "url" : "http://www.example.com/article",
                "type" : "fulltext",
                "content_type" : "HTML"
            }
        ],
        "abstract" : "This is the abstract for the example article. It can be quite a long field so there's a fairly"
                     " sizable chunk of text here. The weather today is grey, because I am writing this from Scotland,"
                     " and the time is early evening. A cup of tea helps work's pleasantness - in particular, a"
                     " rooibos blend with vanilla and spice. It's a tea that goes fairly well with ginger biscuits."
                     " Never dunked, of course. Rooibos is from South Africa; it's a flavoursome caffeine-free tea,"
                     " ideal for the working day. I like mine fairly strong - steeping for 3-4 minutes gives this tea"
                     " enough time to release its distinctive flavour, but without overpowering the delicate vanilla. ",
        "author" : [
            {
                "name" : "The Author",
                "email" : "author@example.com",
                "affiliation" : "University Cottage Labs"
            },
        ],
        "keywords": ["word", "key"],
        "subject" : [
            {
                "scheme": "LCC",
                "term": "Economic theory. Demography",
                "code": "HB1-3840"
            },
            {
                "scheme": "LCC",
                "term": "Social Sciences",
                "code": "H"
            }
        ],
    },
    "created_date": "2000-01-01T00:00:00Z"
}
