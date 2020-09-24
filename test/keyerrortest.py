some_dict = {
    "alphabet": "ABCDEFGHI...Whatever!",
    "flag": True,
    "comment": "What did you expect, bro?",
    "score": 85
}

# try:
#     alphabet = some_dict.get("alphabet")
#     flag = some_dict.get("flag")
#     error = some_dict.get("error")
#     score = some_dict.get("score")
#     comment = some_dict.get("comment")
#
# except KeyError:
#     print(alphabet, flag, error, score, comment)

alphabet = some_dict.get("alphabet") or None
flag = some_dict.get("flag") or None
error = some_dict.get("error") or None
score = some_dict.get("score") or None
comment = some_dict.get("comment") or None

print(alphabet, flag, error, score, comment)
