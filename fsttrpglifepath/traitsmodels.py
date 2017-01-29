from traits.api import HasTraits, String, Button, List, Instance, Int
from traitsui.api import *
from fsttrpgtables.models import Table
from fsttrpgtables.utilities import export_to_aws
from models import event_menu
from random import randint

lc_table = Table('lifepath_shortcuts')


class LifepathShortcutMaker(HasTraits):
    identifier = String()
    chain_string = String()
    decoded_chain = String()
    short_description = String()
    upload = Button()

    def _identifier_changed(self):
        params_array = self.identifier.split('.', -1)
        numbers_array = []
        for param in params_array:
            try:
                numbers_array.append(int(param))
            except ValueError:
                pass
        table = Table('event_menu')
        try:
            chain_string = table.get_result_chain_string(*numbers_array)
            self.chain_string = chain_string
            decoded_chain = table.decode_table_chain_string(chain_string)
            array_of_results = []
            for table in decoded_chain:
                option = table['option']
                array_of_results.append(option.re + " ")

            string_of_results = ''.join(array_of_results)
            self.decoded_chain = string_of_results
        except TypeError:
            print('type-error')

    def _upload_fired(self):
        identifier = self.identifier
        params_array = self.identifier.split('.', -1)
        numbers_array = []
        for param in params_array:
            try:
                int(param)
                numbers_array.append(param)
            except ValueError:
                pass
        numstring = ''.join(numbers_array)
        result = self.chain_string + "@" + self.short_description
        export_to_aws(name='lifepath_shortcuts', identifier=identifier, fr=numstring, to=numstring, re=result,
                      leads_to=None)
        print('done')

    view = View(
        VGroup(
            Item('identifier'),
            Item('chain_string', width=600),
            Item('decoded_chain', width=600),
            Item('short_description'),
            Item('upload', show_label=False)
        )
    )


class Event(HasTraits):
    age = Int()
    path = String()
    desc = String()
    chain = String()
    random_event = Button()

    def _random_event_fired(self):
        r = randint(1, 4)
        chain, array = event_menu.get_random_chain_string(first_index=r)
        string_path = ""

        for cell in array:
            string_path = string_path + str(cell) + '.'

        string_path = string_path[:-1]
        self.path = string_path

    def _path_changed(self):
        path_array = self.path.split('.', -1)
        num_array = []
        for cell in path_array:
            try:
                num_array.append(int(cell))
            except ValueError:
                pass

        self.chain = event_menu.get_result_chain_string(*num_array)
        short_option = lc_table.get_option(identifier=self.path)
        if short_option:
            short_result = short_option.re
            short_array = short_result.split('@')
            self.desc = short_array[1]
        else:
            decoded_chain = event_menu.decode_table_chain_string(self.chain)
            array_of_results = []
            for table in decoded_chain:
                option = table['option']
                array_of_results.append(option.re + " ")

            string_of_results = ''.join(array_of_results)
            self.desc = string_of_results

    view = View(
        HGroup(
            Item('random_event', show_label=False),
            Item('age', width=2),
            Item('path', width=15),

        ),
        Item('desc', width=600, show_label=False),

    )


'''class Lifepath(HasTraits):
    event = Instance(Event, ())

    def _event_default(self):
        return Event(age=16)

    view = View(Group(
        Item('event', style='custom', resizable=True)
    ))'''


class Lifepath(HasTraits):
    events = List(Instance(Event()))

    def _events_default(self):
        events = []
        for i in range(15, 25):
            events.append(Event(age=i))
        return events

    view = View(
        Item('events', show_label=False, editor=ListEditor(style='custom'))
    )


if __name__ == '__main__':
    # l = LifepathShortcutMaker()
    l = Lifepath()
    l.configure_traits()
