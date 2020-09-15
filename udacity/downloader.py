import os
from os.path import join
from urllib.parse import unquote

from .request import Session, GraphQLRequest
from .utils.download import download
from .utils.renderer import Renderer


def mkdirs(path):
    try:
        os.makedirs(path)
    except:
        pass


def download_course(args):
    if len(args.course_id) > 1 and args.flat:
        raise Exception("Can't select `--flat` while downloading multiple courses!")

    for course_id in args.course_id:

        print(f"Start downloading course `{course_id}`", flush=True)

        s = Session.login(args.username, args.password)
        g = GraphQLRequest(s)

        course = g.get_course(course_id)

        outdir = args.outdir

        if not args.flat:
            outdir = join(args.outdir, course_id)

        mkdirs(outdir)

        data = {'course': course}
        html = Renderer().render("CourseHome.html", **data)
        open(join(outdir, "index.html"), "w+").write(html)

        for i, lesson in enumerate(course.lessons, 1):
            data.update(lesson=lesson, lesson_index=i)
            html = Renderer().render("CourseLesson.html", **data)
            open(join(outdir, "lesson-%02d.html") % i, "w+").write(html)

            if args.download_resources and lesson.resources['files']:
                for file in lesson.resources['files']:
                    file_name = file['uri'].split('/')[-1]
                    file_name = file['name'] if file_name == 'download' else file_name
                    dir_name = join(outdir, 'resources', 'lesson-%02d' % i)
                    mkdirs(dir_name)
                    download(file['uri'], join(dir_name, unquote(file_name)))

            for j, concept in enumerate(lesson.concepts, 1):
                data.update(concept=concept, concept_index=j)
                html = Renderer().render("CourseConcept.html", **data)
                open(join(outdir, "concept-%02d-%02d.html") % (i, j), "w+").write(html)


def download_nanodegree(args):
    print(args)
