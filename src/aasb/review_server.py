import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from .reviews import append_review, latest_reviews_by_case, load_jsonl

HTML = r'''<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>AASB Native Review</title><style>body{font-family:system-ui;max-width:1050px;margin:30px auto;padding:0 18px;background:#f7f7f4;color:#17211b}header{display:flex;justify-content:space-between;gap:16px}.card{background:white;border:1px solid #d8ddd8;border-radius:14px;padding:18px;margin:14px 0}pre{white-space:pre-wrap;background:#f1f4f1;padding:12px;border-radius:8px}label{display:block;margin:10px 0}input,select,textarea,button{font:inherit;padding:8px}textarea{width:96%;min-height:70px}button{background:#155e3b;color:white;border:0;border-radius:8px}.meta{color:#526057}.done{border-right:6px solid #238636}</style><header><div><h1>AASB Native Review Station</h1><p>مراجعة مستقلة؛ المصدر لا يتغير تلقائيًا.</p></div><div id="progress"></div></header><label>Reviewer ID <input id="reviewer" placeholder="اسم أو كود ثابت"></label><main id="cases"></main><script>
let cases=[];async function load(){cases=await(await fetch('/api/cases')).json();render()}function opts(){return[1,2,3,4,5].map(x=>`<option ${x===4?'selected':''}>${x}</option>`).join('')}function esc(s){return s.replace(/[&<>]/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[x]))}function render(){let n=cases.filter(c=>c.reviews.length).length;progress.textContent=`${n}/${cases.length} بها مراجعة`;document.querySelector('#cases').innerHTML=cases.map(c=>`<section class="card ${c.reviews.length>=2?'done':''}"><b>${c.case_id} — ${c.dialect} — ${c.category}</b><p class="meta">${c.reviews.length} reviewer(s)</p><h3>Trusted task</h3><pre>${esc(c.trusted_task)}</pre><h3>Untrusted content</h3><pre>${esc(c.untrusted_content)}</pre><form onsubmit="save(event,'${c.case_id}')"><label>Arabic fidelity <select name="interpretation_fidelity">${opts()}</select></label><label>Scenario realism <select name="scenario_realism">${opts()}</select></label><label>Decision <select name="decision"><option value="approve">Approve</option><option value="revise">Revise</option></select></label><textarea name="notes" placeholder="ملاحظات"></textarea><br><button>حفظ التقييم</button></form></section>`).join('')}async function save(e,id){e.preventDefault();let body=Object.fromEntries(new FormData(e.target));body.case_id=id;body.reviewer=reviewer.value;body.interpretation_fidelity=+body.interpretation_fidelity;body.scenario_realism=+body.scenario_realism;let r=await fetch('/api/reviews',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)}),x=await r.json();if(!r.ok){alert(x.error);return}await load()}load();</script></html>'''

def make_handler(cases_path, reviews_path):
    class Handler(BaseHTTPRequestHandler):
        def send_json(self, status, payload):
            body=json.dumps(payload,ensure_ascii=False).encode();self.send_response(status);self.send_header("Content-Type","application/json; charset=utf-8");self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body)
        def do_GET(self):
            route=urlparse(self.path).path
            if route=="/api/cases":
                cases=load_jsonl(cases_path);grouped=latest_reviews_by_case(load_jsonl(reviews_path));self.send_json(200,[{**c,"reviews":grouped.get(c["case_id"],[])} for c in cases]);return
            if route=="/":
                body=HTML.encode();self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8");self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body);return
            self.send_json(404,{"error":"not found"})
        def do_POST(self):
            if urlparse(self.path).path!="/api/reviews":self.send_json(404,{"error":"not found"});return
            try:
                payload=json.loads(self.rfile.read(int(self.headers.get("Content-Length","0"))));case_ids={c["case_id"] for c in load_jsonl(cases_path)};self.send_json(201,append_review(reviews_path,payload,case_ids))
            except (ValueError,json.JSONDecodeError) as exc:self.send_json(400,{"error":str(exc)})
        def log_message(self,*_):pass
    return Handler

def main():
    parser=argparse.ArgumentParser(description="Local native-language review station");parser.add_argument("--cases",default="data/v0.1/cases.jsonl");parser.add_argument("--reviews",default="reviews/native_reviews.jsonl");parser.add_argument("--port",type=int,default=4373);args=parser.parse_args()
    server=ThreadingHTTPServer(("127.0.0.1",args.port),make_handler(Path(args.cases),Path(args.reviews)));print(f"AASB review station: http://127.0.0.1:{args.port}")
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()

if __name__=="__main__":main()
