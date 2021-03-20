from datetime import datetime
from detectweb import db


class Predict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 理论上imgname可能相同，实际上几乎不可能，因此认为unique
    img_name = db.Column(db.String(64), unique=True, index=True)
    img_path = db.Column(db.String(128))
    size = db.Column(db.String(20))
    predict_time = db.Column(db.DateTime, default=datetime.utcnow)
    predict_result = db.Column(db.String(64))
    predict_value = db.Column(db.String(20))
    # 这个user是小写，代表table的名字（默认情况下，table名字为小写的class）
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "id={}, img={}, path={}, body={}, create_time={}, result={}, user_id={}".format(
            self.id, self.img_name, self.img_path, self.size, self.predict_time, self.predict_result, self.user_id
        )
