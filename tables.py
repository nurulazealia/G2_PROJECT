from flask_table import Table, Col, LinkCol

# database table 1 - uploaded files record
class Results(Table):
    id = Col('ID', show=True)
    username = Col('Username')
    title = Col('Filename')
    location = Col('Location')
    date_uploaded = Col('Date Uploaded')
    show = LinkCol('View', 'show', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))

# database table 2 - storage path record
class Paths(Table):
    id = Col('ID', show=True)
    sound_path = Col('Sound Path')
    waveform_path = Col('Waveform Path')
    
# database table 3 - audio file report record
class Reports(Table):
    id = Col('ID', show=True)
    file_duration = Col('Length')
    file_size = Col('File Size')
    file_type = Col('File Type')
    sampling_freq = Col('Sampling Frequency')

# explore table 1 - files uploaded with view hyperlink
class Explore(Table):
    title = Col('Filename')
    location = Col('Location')
    show = LinkCol('View', 'show', url_kwargs=dict(id='id'))
    

