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
    const res = await fetch(`${API_URL}/assessment/test?subject=${subject}&grade=${grade}`, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
    if (!res.ok) throw new Error("Internal Server Error");
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