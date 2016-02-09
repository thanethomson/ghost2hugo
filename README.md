# Ghost2Hugo Converter

## Overview
[Ghost](https://ghost.org/) is a great blogging tool, but sometimes you've just
got to replace it with a static site generator like [Hugo](http://gohugo.io/).
This little utility will help you to do that, but only if your Ghost database is
a SQLite (I haven't written support for MySQL yet, but should be trivial to
extend if you take a look at the code).

It effectively just generates a single Markdown-formatted file for each
post in the Ghost database, and can also generate a single YAML/TOML file for
each user in the Ghost database. You can then easily just copy these files into
your Hugo project and rebuild.

## Usage
1. Clone the repository:
  ```bash
  > git clone https://github.com/thanethomson/ghost2hugo.git
  > cd ghost2hugo
  ```

2. Set up and activate your Python 2.x virtual environment:
  ```bash
  > virtualenv -p python2 .
  > source ./bin/activate
  ```

3. Install dependencies (we just need `pytz` and `tzlocal` for timezone
  adjustment):
  ```bash
  > pip install -r requirements.txt
  ```
4. Run!

  ```bash
  > ./ghost2hugo.py /path/to/ghost.db --post-template=templates/post.md --post-output=./posts \
    --author-template=templates/author.yml --author-output=./authors
  ```

That should use the default template for posts (`templates/post.md`) and
populate the parameters in the template (such as `$title` and `$date`) from
the `posts` and `users` tables in the database (it automatically replaces
`$author` with the author's `slug` field in the `users` table).

Then, it uses the default template for authors (`templates/author.yml`) and
populates the  parameters in that template too from the `users` table in the
Ghost database.

If you don't specify `--author-template` *and* `--author-output`, it will not
extract authors from the database. This applies to the combination of
`--post-template` and `--post-output` too.

## Templates
### Posts
Post output files are labelled according to their slug, with the file extension
of the template file.

The following template variables are available in post templates:
* `$date` - The ISO 8601-formatted timestamp of when the post was last updated
  or published.
* `$title` - The title of the post.
* `$slug` - The post's slug.
* `$author` - The slug of the user who authored this post.
* `$content` - The Markdown content of the post.

### Authors
Sometimes, for multi-author blogs, you need Hugo data files containing author
bios and information. Author output files are labelled according to the user
slugs, with the same file extension as that of the specified template.

The following template variables are available in author templates:
* `$name` - The user's full name.
* `$email` - The user's e-mail address.
* `$bio` - The user's bio.
* `$website` - The user's personal web site.
* `$image` - The unmodified location of the user's profile image. **Note**:
  this script does *not* transform, extract or handle image content in any way -
  that's still unfortunately a manual process at present.

## License
The MIT License (MIT)

Copyright (c) 2016, Thane Thomson.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
