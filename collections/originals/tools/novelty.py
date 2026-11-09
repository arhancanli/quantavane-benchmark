"""Novelty check for Quantavane Originals: arXiv API searches and OEIS searches, written down per problem.

  python3 -I novelty.py SPEC.json OUTDIR RAWDIR

SPEC.json is a list of {"id": PROBLEM, "arxiv": [search_query, ...], "oeis": [terms or words, ...]}. Each arXiv
query is an arXiv API search_query (for example all:"Sidon set" AND all:"sum-free"); each OEIS query is either a
comma-separated list of terms or words. Raw responses are saved in RAWDIR (a fresh, empty directory per run); the
summary for each problem goes to OUTDIR/PROBLEM.json: every query with its address, the time it was run, the number
of results and the first results (arXiv: identifier, year, first author, title; OEIS: A-number and name). Only titles,
identifiers and names are kept; nothing else from the sources is copied. Searching is reading data: nothing is ever
submitted anywhere. arXiv asks for at most one request every 3 seconds; this program waits 3.5 s between requests."""
import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)"}
ATOM = "{http://www.w3.org/2005/Atom}"
OS = "{http://a9.com/-/spec/opensearch/1.1/}"


def fetch(url, raw_path):
    for attempt in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
            with open(raw_path, "wb") as f:
                f.write(data)
            return data
        except Exception as e:  # network trouble: wait and retry
            err = e
            time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"{url}: {err}")


def arxiv(query, raw_path, n=10):
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": query, "start": 0, "max_results": n, "sortBy": "relevance"})
    root = ET.fromstring(fetch(url, raw_path))
    total = int(root.find(OS + "totalResults").text)
    hits = []
    for e in root.findall(ATOM + "entry"):
        aid = e.find(ATOM + "id").text.rsplit("/abs/", 1)[-1]
        title = re.sub(r"\s+", " ", e.find(ATOM + "title").text).strip()
        authors = [a.find(ATOM + "name").text for a in e.findall(ATOM + "author")]
        hits.append({"arxiv": aid, "year": e.find(ATOM + "published").text[:4],
                     "first_author": authors[0] if authors else "", "title": title})
    return {"engine": "arXiv API", "query": query, "url": url, "results": total, "top": hits}


def oeis(query, raw_path):
    url = "https://oeis.org/search?" + urllib.parse.urlencode({"q": query, "fmt": "json"})
    data = json.loads(fetch(url, raw_path) or b"null")
    rows = data if isinstance(data, list) else (data or {}).get("results") or []
    hits = [{"oeis": "A%06d" % r["number"], "name": r.get("name", "")} for r in rows[:10]]
    return {"engine": "OEIS", "query": query, "url": url, "results": len(rows),
            "note": "the JSON search returns at most 10 sequences per page", "top": hits}


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    spec, outdir, rawdir = sys.argv[1:]
    os.makedirs(rawdir, exist_ok=False)          # a fresh directory for every run
    os.makedirs(outdir, exist_ok=True)
    k = 0
    for item in json.load(open(spec)):
        path = os.path.join(outdir, item["id"] + ".json")
        old = json.load(open(path)) if os.path.exists(path) else {"id": item["id"], "searches": []}
        done = {(s["engine"], s["query"]) for s in old["searches"]}
        for engine, queries in (("arXiv API", item.get("arxiv", [])), ("OEIS", item.get("oeis", []))):
            for q in queries:
                if (engine, q) in done:
                    continue
                k += 1
                raw = os.path.join(rawdir, f"{k:04d}.{'xml' if engine == 'arXiv API' else 'json'}")
                r = arxiv(q, raw) if engine == "arXiv API" else oeis(q, raw)
                r["run"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                old["searches"].append(r)
                print(f"{item['id']:28s} {engine:9s} {r['results']:>6d}  {q[:90]}", flush=True)
                time.sleep(3.5)
        with open(path, "w") as f:
            json.dump(old, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
