const clean = value => String(value || "").trim().slice(0, 700);
const schema = { type:"object", additionalProperties:false, required:["title","summary","training","advice"], properties:{ title:{type:"string"}, summary:{type:"string"}, advice:{type:"string"}, training:{type:"array",minItems:2,maxItems:2,items:{type:"object",additionalProperties:false,required:["title","body"],properties:{title:{type:"string"},body:{type:"string"}}}}}};
export default async function handler(req,res) {
  if(req.method!=="POST") return res.status(405).json({error:"method_not_allowed"});
  if(!process.env.OPENAI_API_KEY) return res.status(503).json({error:"not_configured"});
  const body=typeof req.body==="string"?JSON.parse(req.body||"{}"):(req.body||{});
  const answers=Object.fromEntries(Object.entries(body.answers||{}).slice(0,20).map(([k,v])=>[k,{text:clean(v&&v.text),detail:clean(v&&v.detail)}]));
  const scores=Object.fromEntries(Object.entries(body.scores||{}).slice(0,4).map(([k,v])=>[k,Math.max(0,Math.min(100,Number(v)||0))]));
  if(Object.keys(answers).length<6||Object.keys(scores).length<4)return res.status(400).json({error:"invalid_input"});
  const instruction="Sei un advisor AI pragmatico di Iside Systems. "+
  "Rispondi esclusivamente in italiano corretto, in alfabeto latino, con gli accenti al posto giusto "+
  "(perch\u00e9, pi\u00f9, gi\u00e0, qualit\u00e0, priorit\u00e0, \u00e8): mai vocali senza accento al posto di quelle accentate. "+
  "Ti rivolgi all\u0027azienda che ha risposto: non nominare mai Iside Systems come se fosse il cliente. "+
  "Non promettere risultati certi e non inventare dati che non ti sono stati dati. "+
  "Il piano operativo lo scrive gi\u00e0 la pagina e segue sempre questa sequenza: formazione dove manca, "+
  "workshop interni con le business unit, individuazione di tecnologie e colli di bottiglia, stima del ROI "+
  "per iniziativa, due agenti in produzione entro 90 giorni, aggregazione dei dati di marketing dove serve, "+
  "codice di condotta AI e posizionamento su AI Act, GDPR e Digital Services Act. "+
  "Il tuo compito \u00e8 solo la prosa intorno: title breve e concreto; summary di 4-6 righe che legge i "+
  "punteggi e le risposte e dice qual \u00e8 l\u0027anello debole; training con esattamente 2 voci, la prima di "+
  "alfabetizzazione AI per tutta l\u0027azienda, la seconda mirata sulle funzioni pi\u00f9 sotto pressione secondo "+
  "le risposte, con esempi del loro settore; advice, il primo passo, coerente con la sequenza sopra. "+
  "Ogni body al massimo 230 caratteri."
  try {
    const upstream=await fetch("https://api.openai.com/v1/responses",{method:"POST",headers:{"Content-Type":"application/json",Authorization:"Bearer "+process.env.OPENAI_API_KEY},body:JSON.stringify({model:process.env.OPENAI_MODEL||"gpt-4.1-mini",store:false,max_output_tokens:1200,input:instruction+"\nPUNTEGGI: "+JSON.stringify(scores)+"\nRISPOSTE: "+JSON.stringify(answers),text:{format:{type:"json_schema",name:"ai_maturity_report",strict:true,schema}}})});
    if(!upstream.ok){console.error("ai-maturity upstream",upstream.status,(await upstream.text()).slice(0,300));return res.status(502).json({error:"model_failed"});}
    const payload=await upstream.json();
    // output_text is an SDK convenience field; the REST payload only carries the
    // message items, so read the text out of those
    const text=(payload.output||[]).filter(o=>o.type==="message").flatMap(o=>o.content||[]).filter(c=>c.type==="output_text").map(c=>c.text).join("");
    if(!text){console.error("ai-maturity empty output",payload.status,JSON.stringify(payload.incomplete_details||{}));return res.status(502).json({error:"model_failed"});}
    // a model that slips a Cyrillic or CJK word into the copy is worse than the
    // local fallback, which the client already carries
    if(/[\u0400-\u04FF\u0370-\u03FF\u4E00-\u9FFF\u3040-\u30FF]/.test(text)){console.error("ai-maturity non-latin output");return res.status(502).json({error:"model_failed"});}
    return res.status(200).json(JSON.parse(text));
  } catch(error) { console.error("ai-maturity",error.message);return res.status(502).json({error:"model_failed"}); }
}
