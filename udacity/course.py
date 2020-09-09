from udacity import atoms
from udacity.utils.object_dict import ObjectDict
from udacity.utils.renderer import ClassRenderer


class Course(ClassRenderer):
    def __init__(self, seq=None, **kwargs) -> None:
        super().__init__(seq, **kwargs)
        self['lessons'] = [self.Lesson(self, lesson) for lesson in self['lessons']]

    def iter_lessons(self):
        for lesson in self.lessons:
            yield lesson

    def iter_concepts(self):
        for lesson in self.iter_lessons():
            for concept in lesson.concepts:
                yield concept

    def iter_atoms(self):
        for concept in self.iter_concepts():
            for atom in concept.atoms:
                yield atom

    class Lesson(ClassRenderer):
        def __init__(self, course, seq=None, **kwargs):
            super().__init__(seq, **kwargs)
            self.course = course
            self['concepts'] = [self.Concept(self, concept) for concept in self['concepts']]

        class Concept(ClassRenderer):
            def __init__(self, lesson, seq=None, **kwargs):
                super().__init__(seq, **kwargs)
                self.lesson = lesson
                create_atom = lambda atom: getattr(atoms, atom['semantic_type'])(atom, concept=self)
                self['atoms'] = [create_atom(atom) for atom in self['atoms']]
