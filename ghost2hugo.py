#!/usr/bin/env python
"""
Dumps the contents of a Ghost SQLite database to files that Hugo can
understand.
"""
import sqlite3
import argparse
from copy import copy
from datetime import datetime
from pytz import utc
from tzlocal import get_localzone
import os
import os.path


def read_template(filename):
    """
    Reads content from the given file.
    """
    content = None

    with open(filename, 'rt') as f:
        content = f.read().encode('UTF-8', 'replace')

    return content


def render_template(content, ctx):
    """
    Parses the given template content and replaces keywords using the specified
    context dictionary.
    """
    _content = copy(content)
    if _content:
        for k, v in ctx.iteritems():
            _content = _content.replace('$%s' % k, v.encode('UTF-8', 'replace'))
    else:
        _content = ''

    return _content


def extract_posts(conn, template, output_dir):
    """
    Extracts all of the posts in Markdown format to the specified output
    directory.
    """
    tz = get_localzone()
    template_filename, template_ext = os.path.splitext(template)
    template_content = read_template(template)
    # ensure that the output path exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for row in conn.execute('SELECT posts.title, posts.slug, posts.markdown, ' +\
        'posts.updated_at, posts.published_at, '+\
        'users.slug FROM ' +\
        'posts INNER JOIN users on author_id=users.id'):
        ctx = {
            'date'   : '',
            'title'  : '',
            'slug'   : '',
            'author' : '',
            'content': '',
        }
        vals = list(row)
        if vals[4]:
            ctx['date'] = utc.localize(datetime.fromtimestamp(vals[4] / 1000.0)).astimezone(tz).isoformat()
        elif vals[3]:
            ctx['date'] = utc.localize(datetime.fromtimestamp(vals[3] / 1000.0)).astimezone(tz).isoformat()

        if vals[0]:
            ctx['title'] = vals[0]
        if vals[1]:
            ctx['slug'] = vals[1]
        if vals[5]:
            ctx['author'] = vals[5]
        if vals[2]:
            ctx['content'] = vals[2]

        content = render_template(template_content, ctx)
        # write the post to a file
        output_file = os.path.join(output_dir, '%s%s' % (ctx['slug'], template_ext))
        print "Writing post:", output_file

        with open(output_file, 'w') as f:
            f.write(content)



def extract_authors(conn, template, output_dir):
    """
    Extracts all of the users and outputs them according to the specified
    template.
    """
    template_filename, template_ext = os.path.splitext(template)
    template_content = read_template(template)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for row in conn.execute('SELECT name, slug, email, image, bio, website FROM users'):
        vals = list(row)
        ctx = {
            'name'    : vals[0] or '',
            'slug'    : vals[1] or '',
            'email'   : vals[2] or '',
            'image'   : vals[3] or '',
            'bio'     : vals[4] or '',
            'website' : vals[5] or '',
        }

        content = render_template(template_content, ctx)
        # write the author to a file
        output_file = os.path.join(output_dir, '%s%s' % (ctx['slug'], template_ext))
        print "Writing author:", output_file

        with open(output_file, 'w') as f:
            f.write(content)


def main():
    """
    Our main program routine.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('db',
        help='The SQLite3 database from which to extract data')
    parser.add_argument('--post-template',
        help='The template file to use for extracting posts')
    parser.add_argument('--post-output',
        help='The path to which to output posts')
    parser.add_argument('--author-template',
        help='The template file to use for extracting authors')
    parser.add_argument('--author-output',
        help='The path to which to output posts')

    args = parser.parse_args()

    # try to connect to the database
    conn = sqlite3.connect(args.db)

    try:
        if args.post_template is not None and args.post_output is not None:
            print "Extracting post(s) from database..."
            extract_posts(conn, args.post_template, args.post_output)

        if args.author_template is not None and args.author_output is not None:
            print "Extracting author(s) from database..."
            extract_authors(conn, args.author_template, args.author_output)

    except:
        import traceback
        traceback.print_exc()

    conn.close()


if __name__ == "__main__":
    main()
