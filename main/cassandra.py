from cassandra.cluster import Cluster

cluster = Cluster()
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()
session.set_keyspace('db')

delete_by_artist_stmt = session.prepare("delete from db.song_by_artist where id_song=? and id_artist=?")
delete_by_album_stmt = session.prepare("delete from db.song_by_album where id_song=? and id_album=?")
delete_by_genre_stmt = session.prepare("delete from db.song_by_genre where id_song=? and id_genre=?")
delete_by_label_stmt = session.prepare("delete from db.song_by_label where id_song=? and id_label=?")
select_by_artist_stmt = session.prepare("select * from db.song_by_artist where id_artist=?")
select_by_album_stmt = session.prepare("select * from db.song_by_album where id_album=?")
select_by_genre_stmt = session.prepare("select * from db.song_by_genre where id_genre=?")
select_by_label_stmt = session.prepare("select * from db.song_by_label where id_label=?")
