import argparse
from os.path import join

from udacity.request import *
from udacity.utils.renderer import Renderer

parser = argparse.ArgumentParser(description='Download udacity course')

parser.add_argument('course_id', type=str, help='Course ID')

parser.add_argument('--outdir', '-o', required=True, type=str, help='Output directory')

parser.add_argument("--username", "-u", required=True, type=str, help="Udacity account username/email")
parser.add_argument("--password", "-p", required=True, type=str, help="Udacity account password")


def main():
    args = parser.parse_args()

    s = Session.login(args.username, args.password)
    g = GraphQLRequest(s)

    course = g.get_course(args.course_id)

    html = Renderer().render("CourseHome.html", course=course)
    open(join(args.outdir, "index.html"), "w+").write(html)

    for i, lesson in enumerate(course.lessons, 1):
        html = Renderer().render("CourseLesson.html",
                                 course=course, lesson=lesson, lesson_index=i, )
        open(join(args.outdir, "lesson-%02d.html") % i, "w+").write(html)
        for j, concept in enumerate(lesson.concepts, 1):
            html = Renderer().render("CourseConcept.html",
                                     course=course,
                                     lesson=lesson, lesson_index=i,
                                     concept=concept, concept_index=j)
            open(join(args.outdir, "concept-%02d-%02d.html") % (i, j), "w+").write(html)


if __name__ == '__main__':
    main()
