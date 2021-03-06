from brave.inputs.input import Input


class TestVideoInput(Input):
    def has_audio(self):
        return False

    def permitted_props(self):
        return {
            **super().permitted_props(),
            'pattern': {
                'type': 'int',
                'default': 0
            },
            'width': {
                'type': 'int',
                'default': 640
            },
            'height': {
                'type': 'int',
                'default': 360
            },
            'xpos': {
                'type': 'int',
                'default': 0
            },
            'ypos': {
                'type': 'int',
                'default': 0
            },
            'zorder': {
                'type': 'int',
                'default': 1
            }
        }

    def create_elements(self):
        pipeline_string = ('videotestsrc is-live=true name=videotestsrc'
                           ' ! videoconvert ! videoscale ! capsfilter name=capsfilter' +
                           self.default_video_pipeline_string_end())
        # FOR TESTING TO VIEW LOCALLY, APPEND: + ' final_video_tee. ! queue ! glimagesink ')
        if not self.create_pipeline_from_string(pipeline_string):
            return False

        self.final_video_tee = self.pipeline.get_by_name('final_video_tee')
        self.videotestsrc = self.pipeline.get_by_name('videotestsrc')
        self.capsfilter = self.pipeline.get_by_name('capsfilter')
        self.handle_updated_props()

    def handle_updated_props(self):
        super().handle_updated_props()
        if 'pattern' in self.props:
            self.videotestsrc.set_property('pattern', self.props['pattern'])
