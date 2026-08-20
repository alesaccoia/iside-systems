const clean = value => String(value || "").trim().slice(0, 700);
const schema = { type:"object", additionalProperties:false, required:["title","summary","wins","advice"], properties:{ title:{type:"string"}, summary:{type:"string"}, advice:{type:"string"}, wins:{type:"array",minItems:3,maxItems:3,items:{type:"object",additionalProperties:false,required:["title","body"],properties:{title:{type:"string"},body:{type:"string"}}}}}};
export default async function handler(req,res) {
  if(req.method!=="POST") return res.status(405).json({error:"method_not_allowed"});
  if(!process.env.OPENAI_API_KEY) return res.status(503).json({error:"not_configured"});
  const body=typeof req.body==="string"?JSON.parse(req.body||"{}"):(req.body||{});
  const answers=Object.fromEntries(Object.entries(body.answers||{}).slice(0,12).map(([k,v])=>[k,{text:clean(v&&v.text),detail:clean(v&&v.detail)}]));
  const scores=Object.fromEntries(Object.entries(body.scores||{}).slice(0,4).map(([k,v])=>[k,Math.max(0,Math.min(100,Number(v)||0))]));
  if(Object.keys(answers).length<6||Object.keys(scores).length!==4)return res.status(400).json({error:"invalid_input"});
  const instruction="Sei un advisor AI pragmatico di Iside Systems. Rispondi in italiano per una PMI. Non promettere risultati certi. Dai priorità a processi reali, dati, adozione e governance. wins contiene esattamente 3 quick win realizzabili nei prossimi 90 giorni; ogni body massimo 230 caratteri.";
  try {
    const upstream=await fetch("https://api.openai.com/v1/responses",{method:"POST",headers:{"Content-Type":"application/json",Authorization:"Bearer "+process.env.OPENAI_API_KEY},body:JSON.stringify({model:process.env.OPENAI_MODEL||"gpt-4.1-mini",store:false,max_output_tokens:900,input:instruction+"\nPUNTEGGI: "+JSON.stringify(scores)+"\nRISPOSTE: "+JSON.stringify(answers),text:{format:{type:"json_schema",name:"ai_maturity_report",strict:true,schema}}})});
    if(!upstream.ok)return res.status(502).json({error:"model_failed"});
    const payload=await upstream.json();return res.status(200).json(JSON.parse(payload.output_text));
  } catch(error) { console.error("ai-maturity",error.message);return res.status(502).json({error:"model_failed"}); }
}
