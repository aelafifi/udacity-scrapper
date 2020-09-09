from . import atoms
from .utils.jinja import jinjaEnv
from .utils.object_dict import ObjectDict
from .utils.renderer import ClassRenderer


class Nanodegree(ObjectDict):
    def __init__(self, seq=None, **kwargs) -> None:
        super().__init__(seq, **kwargs)
        self['parts'] = [self.Part(self, part) for part in self['parts']]

    def iter_parts(self):
        for part in self.parts:
            yield part

    def iter_modules(self):
        for part in self.iter_parts():
            for module in part.modules:
                yield module

    def iter_lessons(self):
        for module in self.iter_modules():
            for lesson in module.lessons:
                yield lesson

    def iter_concepts(self):
        for lesson in self.iter_lessons():
            for concept in lesson.concepts:
                yield concept

    def iter_atoms(self):
        for concept in self.iter_concepts():
            for atom in concept.atoms:
                yield atom

    class Part(ClassRenderer):
        def __init__(self, nanodegree, seq=None, **kwargs):
            super().__init__(seq, **kwargs)
            self.nanodegree = nanodegree
            self['modules'] = [self.Module(self, module) for module in self['modules']]

        class Module(ClassRenderer):
            def __init__(self, part, seq=None, **kwargs):
                super().__init__(seq, **kwargs)
                self.part = part
                self['lessons'] = [self.Lesson(self, lesson) for lesson in self['lessons']]

            class Lesson(ClassRenderer):
                def __init__(self, module, seq=None, **kwargs):
                    super().__init__(seq, **kwargs)
                    self.module = module
                    self['concepts'] = [self.Concept(self, concept) for concept in self['concepts']]

                class Concept(ClassRenderer):
                    def __init__(self, lesson, seq=None, **kwargs):
                        super().__init__(seq, **kwargs)
                        self.lesson = lesson
                        create_atom = lambda atom: getattr(atoms, atom['semantic_type'])(atom, concept=self)
                        self['atoms'] = [create_atom(atom) for atom in self['atoms']]
