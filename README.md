# Clean_PC



### Description

Clean_PC is a script that will help you to clean your pc's logs.



### Technology used

* Python 3.6.0
* SQLite3



### Challenges I got

With that project, I just figured out how to use the `sqlite3`'s Python's modules. Beside it, i also learned how to `argparse` which allow you to parse arguments easier.



## Usage

```bash
~/Documents/clean_pc main*
❯ ./clean_pc.py -h
usage: clean_pc.py [-h] [-p PATH] [-s] [-S] [--display-db DISPLAY_DB] [-d] [-b] [-l] [--save SAVE]

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  list all files in the given path
  -s, --size            display the size of the file beside the name
  -S, --sort            display the files from the littlest size to the biggest size
  --display-db DISPLAY_DB
                        display the database's table if there's one
  -d, --date            display the last time the file was modificated
  -b, --big             display the biggest file
  -l, --little          display the littlest file
  --save SAVE           save file's data in a sqlite database (the given file)

	
```



If you run:

```bash
~/Documents/clean_pc main*
❯ ./clean_pc.py   
```

It'll just list all the files you have in the `/var/log` folder.



If you want to save your size with a checkpoint, just run:

```bash
~/Documents/clean_pc main*
❯ ./clean_pc.py --save table         
```



Then you'll have a `table.db` file which contains the filename and their size in the given path



You can put your own path by typing:

```bash
~/Documents/clean_pc main*
❯ ./clean_pc.py -p ~/ --save test
```

