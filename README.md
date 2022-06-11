# create_deck

This module is responsible for creating Anki flashcards for 2anki.net.

## API

The current implementation is CLI driven. [create_deck](./create_deck.py) is
to be executed with two arguments: absolute path to a JSON payload and template directory.
Note that the working directory has to be the workspace directory (location of payload).

Here is an example execution
```bash
$ cd /tmp/w/9dOax-Y1fhrsmZxPad5g5
$ ./create_deck.py \
    /tmp/w/9dOax-Y1fhrsmZxPad5g5/deck_info.json
    /Users/scanf/src/github.com/2anki/server/src/templates/
```

Here is the workspace directory (stripped long filenames)
As you can see above there are also media files in here.
The apkg file is created based on the contents of deck_info.json.

```
/tmp/w/9dOax-Y1fhrsmZxPad5g5
├── [...].png
├── [...].apkg
├── [...].jpg
├── [...].png
├── [...].jpg
└── deck_info.json
```

### JSON Structure

Inside of the deck_info.json is an array of decks.
A deck consists of settings (object), name (string), cards (array), image (string), style (string)

TODO: roadmap
