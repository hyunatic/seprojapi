CREATE TABLE "Post" (
	"Postid"	INTEGER,
	"Userid"	INTEGER,
	"ItemName"	BLOB,
	"Category"	TEXT,
	"Description"	TEXT,
	"ImageId"	TEXT,
	PRIMARY KEY("Postid" AUTOINCREMENT),
	FOREIGN KEY("Userid") REFERENCES auth_user(id) );