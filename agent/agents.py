import time



def llm(client,MODEL,messages, temperature=0.4, max_tokens=600, retries=3):
  last_err = None
  for i in range(retries):
    try:
      resp = client.chat.completions.create(
          model = MODEL,
          messages = messages,
          temperature = temperature,
          max_tokens = max_tokens,
          stream = False,
      )
      return (resp.choices[0].message.content or "").strip()
    except Exception as e:
      last_err = e
      backoff = 2 ** i
      print(f"[!] API error: {e} - retrying in {backoff}s...", flush=True)
      time.sleep(backoff)
  raise last_err

def thinking(msg="Agent is thinking", ticks=3, delay=0.5):
  print(msg, end="", flush=True)
  for _ in range(ticks):
    time.sleep(delay)
    print(".", end="", flush=True)
  print("\n", flush=True)

SYSTEM = (
    "You are an autonomous research agent using strict ReAct.\n"
    "- Thought: concise reasoning and sub-questions (<=120 words).\n"
    "- Action: choose exactly ONE: THINK, DRAFT, FINISH, WEB_SEARCH.\n"
    "- WEB_SEARCH: use for external data, trends, market info, or competitor info.\n"
    "- Observation: summarize what that action plausibly yields from knowledge or web search.\n"
    "- Return ONLY the Thought/Action/Observation for each step, no extra text."
)

def gen_thought(client,MODEL,topic, prev_observations):
  memory_text = "\n".join([f"- {o}" for o in prev_observations]) if prev_observations else "(none)"
  user = f"Topic: {topic}\nPrevious observations:\n{memory_text}\n\nProduce the next Thought only."
  return llm(client,MODEL,[{"role":"system", "content":SYSTEM},{"role":"user", "content":user}], temperature=0.5)

def gen_action(client,MODEL,topic, thought, prev_observations):
  memory_text = "\n".join([f"- {o}" for o in prev_observations]) if prev_observations else "(none)"
  user = f"Topic: {topic}\nThought: {thought}\nPrevious observations: \n{memory_text}\n\nProduce exactly ONE Action (THINK/DRAFT/FINISH/WEB_SEARCH)."
  return llm(client,MODEL,[{"role":"system", "content":SYSTEM},{"role":"user", "content":user}], temperature=0.5)

def gen_observation(client,MODEL,exa,topic, action, query=None):
  if action == "WEB_SEARCH" and query:
    response = exa.search_and_contents(
        query,
        text=True,
        type="auto"
    )
    results = response.results[:3] if hasattr(response, "results") else []
    summary = "\n".join([f"- {getattr(r, 'title', 'No Title')}: {getattr(r, 'content', 'No Content')[:300]}"
                        for r in results
    ])
    return f"Web search results:\n{summary}" if summary else "Web search yielded no useful results"
  else:
    user = f"Topic: {topic}\nAction: {action}\n\nProduce concise Observation only"
    return llm(client,MODEL,[{"role":"system", "content":SYSTEM},{"role":"user", "content":user}], temperature=0.4)

def gen_final_report(client,MODEL,topic, steps):
  notes = []
  for i, s in enumerate(steps, 1):
    notes.append(f"[Step {i}] Thought: {s['thought']}\n[Step {i}] Action: {s['action']}\n[Step {i}] Observation: {s['observation']}\n")
    user = (
        f"Create a concise final report on '{topic}' from these notes:\n\n" +
        "\n".join(notes) +
        "\n\nInclude sections: Executive Summary, Key Findings (bullets), Brief Analysis, Next Steps. Keep it crisp"
    )
  return llm(client,MODEL,[{"role":"system", "content":"You are a precise technical writer."}, {"role":"user","content":user}], temperature=0.3, max_tokens=1500)

def react_agent(client,MODEL,exa,topic, max_steps=4, pause=1.0):
  steps = []
  prev_observations = []
  print(f"\n[*] Running agentic ReAct search on: {topic}\n", flush=True)
  for step in range(1, max_steps+1):
    print(f"[Step {step}] Starting cycle\n", flush=True)
    thinking("Agent is thinking", ticks=3, delay=pause/2)
    thought = gen_thought(client,MODEL,topic, prev_observations)
    thought_clean = thought.replace("Thought:", "").strip()
    print(f"[Step {step}] Thought:\n{thought_clean}\n", flush=True)
    time.sleep(pause)

    thinking("Agent is planning an action", ticks=2, delay=pause/2)
    action = gen_action(client,MODEL,topic, thought_clean, prev_observations)
    action_clean = action.strip().upper()
    print(f"[Step {step}] Action:\n{action_clean}\n", flush=True)
    time.sleep(pause)

    thinking("Agent is deriving an observation", ticks=2, delay=pause/2)
    if action_clean == "WEB_SEARCH":
      observation = gen_observation(client,MODEL,exa,topic, action_clean, query=thought_clean)
    else:
      observation = gen_observation(client,MODEL,exa,topic, action_clean)
    print(f"[Step {step}] Observation:\n{observation}\n", flush=True)
    print("-"*80 + "\n", flush=True)
    prev_observations.append(observation)
    steps.append({"thought": thought_clean, "action": action_clean, "observation": observation})
  report = gen_final_report(client,MODEL,topic, steps)
  return report

