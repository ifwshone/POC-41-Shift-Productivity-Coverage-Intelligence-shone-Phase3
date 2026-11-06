import os,sys,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
os.environ['GEMINI_API_KEY']='dummy-test-key'
import assistant_harness as h
cases=[("grounded","Facility A Night Watch averages 93.6 units/hr, 25.8 below the baseline."),
       ("invented number 7","Facility A Night Watch lost 7 hours of output last week."),
       ("invented number 28","Overtime is 28 hours above plan."),
       ("invented 119.9","Baseline is 119.9 units/hr."),
       ("wrong rank","facility_a_night_watch ranks 2 overall."),
       ("prediction","Output will be lower next week."),
       ("RAISE","RAISE")]
for name,txt in cases:
    h.MODE['text']=txt
    r=h.ask("Why is facility_a_night_watch ranked 1?")
    print(json.dumps({"case":name,"status":r["status"],"llm_status":r["llm_status"],"llm_shown":bool(r["llm_explanation"])}))
