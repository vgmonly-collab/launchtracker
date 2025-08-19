Launch {
  id: str
  title: str
  customer: str
  launch_month: str
  signoff_date: str|null
  content_in_date: str|null
  content_signoff_date: str|null
  next_step: str
  delayed_at: str|null
  status: str
  timeline: Action[]
}

Action {
  ts: str
  actor: str
  role: str
  type: str
  payload: object
}
