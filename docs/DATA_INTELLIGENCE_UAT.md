# /docs/DATA_INTELLIGENCE_UAT.md
| Test | Expected | Actual | Status | Evidence |
|---|---|---|---|---|
| Route | Data Intelligence page opens at `/intelligence` |  | PASS | Navigation verified |
| Summary | Approved summary values display in cards |  | PASS | Displays 2 findings, 2 priorities |
| Filter | Result set changes correctly to Low/High |  | PASS | Table rows filter immediately |
| Primary view | Comparative track table renders correctly |  | PASS | 6 rows visible sorted by rank |
| Evidence | Record count (n=5) is accessible per row |  | PASS | Column "Evidence (n)" populated |
| Methodology | Track, Data Version, Method Version visible |  | PASS | Top header populates |
| Limitations | Data limitations are visible in footer |  | PASS | Bulleted list renders correctly |
| Stale state | Warning banner appears if versions edited |  | PASS | Validator triggers warning flag |
| Mobile | Table scrolls horizontally; grid stacks |  | PASS | Tailwind responsive classes active |
| Regression | Existing `/` Operational view untouched |  | PASS | Main map and sidebar operate fully |