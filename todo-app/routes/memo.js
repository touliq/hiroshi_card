var express = require('express');
var router = express.Router();

var sqlite3 = require('sqlite3');

//データベースオブジェクトの取得
const db = new sqlite3.Database('memo_data.sqlite3');

router.get('/', function(req, res, next) {
    db.serialize(() => {
        //SQL文, memosテーブルから全てのレコードを取得する（* は全て）
        db.all("select * from raikyaku", (err, rows) => {
	    console.log(JSON.stringify(rows));
            if (!err) {
                const data = {
                    title: 'データベース',
                    content: rows //DataBaseから返された全レコードがrowsに配列で入ります
                }
                //viewファイルのmemo/indexにdataオブジェクトが渡されます
                //res.render(テンプレートファイル名, { 渡す値をオブジェクトで }) → テンプレートファイルを描画する
                res.render('memo/index', data);
            }
        })
    })
});

/*router.get('/add', function(req, res, next) {
    const data = {
        title: '追加',
        content: '新しいデータを入力してください'
    }
    res.render('memo/add', data);
});

router.post('/add', function(req, res, next) {
    const tx = req.body.text;
    //SQL文, DataBaseのレコード作成
    db.run('insert into memos (text) values (?)', tx)
    //res.redirect() 引数に指定したアドレスにリダイレクト
    res.redirect('/memo');
});

router.get('/edit', function(req, res, next) {
    const id = req.query.id;
    db.serialize(() => {
        const q = "select * from memos where id = ?";
        db.get(q, [id], (err, row) => {
            if (!err) {
                const data = {
                    title: '更新',
                    content: 'id = ' + id + 'のレコードを更新',
                    memoData: row
                }
                res.render('memo/edit', data);
            }
        })
    })
});

router.post('/edit', function(req, res, next) {
    //POST送信された値はreq.body内にまとまられている
    const id = req.body.id;
    const tx = req.body.text;
    const q = "update memos set text = ? where id = ?";
    db.run(q, tx, id);
    res.redirect('/memo');
});*/

router.get('/table-delete',function(req, res, next){
    const data = {
	title: 'テーブル削除',
	content: 'テーブルを削除します'
    }
    res.render('memo/table-delete', data);
});

router.post('/table-delete',function(req,res,next){
    db.run('delete from raikyaku')
    res.redirect('/memo');
});

router.get('/delete', function(req, res, next) {
    const id = req.query.id;
    db.serialize(() => {
        const q = "select * from raikyaku where id = ?";
        db.get(q, [id], (err, row) => {
            if (!err) {
                const data = {
                    title: '削除',
                    content: 'id = ' + id + 'のメモを削除しますか？',
                    memoData: row
                }
                res.render('memo/delete', data);
            }
        })
    })
});

router.post('/delete', function(req, res, next) {
    const id = req.body.id;
    const q = "delete from raikyaku where id = ?";
    db.run(q, id);
    res.redirect('/memo');
});


module.exports = router;

