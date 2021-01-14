from flask_table import Table, Col, LinkCol

class Results(Table):
    id = Col('ID', show=True)
    title = Col('Filename')
    date_uploaded = Col('Date Uploaded')
    show = LinkCol('View', 'show', url_kwargs=dict(id='id'))
    edit = LinkCol('Edit', 'update', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))