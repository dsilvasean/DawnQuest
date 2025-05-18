const API_URL = process.env.NEXT_PUBLIC_API_URL;


export const fetchUserProfile = async (token:string) => {
    const res = await fetch(`${API_URL}/user`, {
        method:'GET',
        headers:{
          'Authorization': `Bearer ${token}`,
          'Content-Type':"application/json",
        }
      });
      if (!res.ok) throw new Error("Unauthorized!");
      return res.json() 
}

export const fetchSubjects = async (board: number, grade: number)=>{
    const res = await fetch(`${API_URL}/subjects/${board}/${grade}`,{
        headers:{
          'Content-Type':"application/json",
        }
      });
    if (!res.ok) throw new Error("Internal Server Error");
    return res.json() 
}


export const fetchPatterns = async (subject: number, grade: number, token:string)=>{
  console.log("i was called")
    const res = await fetch(`${API_URL}/paper-formats/${subject}/${grade}`, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
    if (!res.ok) throw new Error("Internal Server Error");
    console.log(res)
    return res.json() 
}

export const fetchChapters = async (subject: number,)=>{
    const res = await fetch(`${API_URL}/chapters/${subject}`, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
    if (!res.ok) throw new Error("Internal Server Error");
    return res.json() 
}

export const fetchAssesment  = async(id:number, token:string) =>{
  const res = await fetch(`${API_URL}/assessments/${id}`,{
    headers:{
      'Authorization': `Bearer ${token}`,
      "Content-Type":"application/json"},
  });
  if (!res.ok) throw new Error("Internal Server Error");
  return res.json() 

}


export const generateAssessment = async(format:number, chapters:string[], token:string )=>{
  const payload = {
    format_id: format,
    chapters: chapters
  }
  const res = await fetch(`${API_URL}/assessments/`, {
    method:"POST",
    headers:{
      'Authorization': `Bearer ${token}`,
      "Content-Type":"application/json"},
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("Internal Server Error");
  return res.json() 

}
