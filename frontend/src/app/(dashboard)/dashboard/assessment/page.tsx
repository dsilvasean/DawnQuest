"use client";
import React, { useEffect, useState } from "react";
import { Info } from 'lucide-react';
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "react-toastify";
import Loader from "@/components/custom/Loader";
import FormCard from "@/components/custom/FormCard";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button"; // adjust import as per your setup

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { motion, AnimatePresence } from "framer-motion";


interface Student {
  name:string;
  grade:number;
  board:number;
  board_display:string;
  email:string;
}
interface Subjects {id:number; name:string}
interface PaperFormat {id:number; description:string}


const Assessment = () => {
  const API_URL = process.env.NEXT_PUBLIC_API_URL
  const [token, setToken] = useState<string |null>(null);
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [paperFormat, setPaperFormat] = useState<PaperFormat[]>([]);
  const [student, setStudent] = useState<Student | null>(null);
  const [subjects, setSubjects] = useState<Subjects[]>([]);
  const [step, setStep] = useState<1 | 2 | 3>(1);

  const [selectedSubject, setSelectedSubject] = useState("");
  const [selectedPaperFormat, setSelectedPaperFormat] = useState("");

  const [selectedSubjectId, setSelectedSubjectId] = useState<number | null>(null);

  // const token = localStorage.getItem("access_token");

  
  useEffect(() => {
    const tokenFromStorage = localStorage.getItem("access_token");
    if (!tokenFromStorage) {
      setLoading(true);
      toast.error("Unauthorized");
      setTimeout(() => router.push("/login"), 3000);
    } else {
      console.log(tokenFromStorage)
      setToken(tokenFromStorage);
    }
  }, []);
  
  
  

  useEffect(()=>{

    if (!token) return;

    fetch(`${API_URL}/user`, {
      method:'GET',
      headers:{
        'Authorization': `Bearer ${token}`,
        'Content-Type':"application/json",
      }
    }).then(res => {
      if(!res.ok){
        toast.error("Unauthorized");
        return;
      }
      return res.json();
    }).then(data => {
      const studentObj : Student = {
        name :"hello",
        email:data.data.email,
        grade:data.data.grade.grade,
        board:data.data.board.id,
        board_display:data.data.board.board_display
      }
      setStudent(studentObj)
    })

    

  }, [token]);

  useEffect(()=>{
    if(student?.board && student?.grade){
      fetch(`${API_URL}/subjects/${student.board}/${student.grade}`,{
                headers:{
                  'Content-Type':"application/json",
                }
              }).then(res=>res.json()).then((data)=>{
                setSubjects(data);
                console.log(data)
              })
    }
  }, [student])
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
  };

  const handleNext = async (e: React.FormEvent) => {
    e.preventDefault();
    // setLoading(true);
    if(!selectedSubject){
      toast.error("Please select a subject first");
      return;
    }
    const res = await fetch(`${API_URL}/assessment/test?subject=${selectedSubjectId}&grade=${student?.grade}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    if (!res.ok) {
      toast.error("Failed to fetch patterns");
      return;
    }
    const data = await res.json();
    setPaperFormat(data.data); // update your patterns state
    setStep(2); // go to the next step
  };

  const handleBack = (e:React.FormEvent) => {
    e.preventDefault();
    setStep(1);
  }
  


  useEffect(()=>{
    
  }, [step])

  return (
    
    <>

     <div className="relative overflow-hidden w-full">
    
     <div
      className="flex transition-transform duration-500"
      style={{ transform: `translateX(-${(step - 1) * 100}vw)` }}
    >

      <div className="w-[100vw] px-4 flex-shrink-0">
          <FormCard
            title="Assessment"
            onSubmit={handleNext}
            loading={loading}
            buttonText="Next"
          >
            <div className="grid gap-3">
              <Label>Board</Label>
              <Input
                value={student?.board_display ?? ""}
                disabled
                className="focus-visible:ring-2 focus-visible:ring-brand"
              />
              <Label>Grade</Label>
              <Input
                value={student?.grade ?? ""}
                disabled
                className="focus-visible:ring-2 focus-visible:ring-brand"
              />
              <Label>Subject</Label>
              <Select value={selectedSubject} onValueChange={(value)=>{
                setSelectedSubject(value);
                console.log(subjects)
                console.log(value)
                const selected = subjects.find(subject=>{
                  return subject.name === value
                })
                console.log(selected)
                if(selected){
                  setSelectedSubjectId(selected.id)
                }
              }}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select Subject" />
                </SelectTrigger>
                <SelectContent>
                  {subjects.map((subject) => (
                    <SelectItem key={subject.id} value={subject.name}>
                      {subject.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </FormCard>
        </div>
        <div className="w-[100vw] px-4 flex-shrink-0">
        <FormCard
            title="Select Paper Format"
            onSubmit={(e) => {
              e.preventDefault();
              toast.success("Form submitted!");
              setStep(3)
            }}
            loading={loading}
            buttonText="Submit"
          >
            <div className="grid gap-3">
              <Label>Paper Format</Label>
              <Select value={selectedPaperFormat} onValueChange={setSelectedPaperFormat}>
                
                          <SelectTrigger className="w-full"><SelectValue placeholder="Select Paper Format" /></SelectTrigger>
                          
                          <SelectContent>
                          
                            {paperFormat.map(format => (
                              <SelectItem key={format.id} value={format.description.toString()}>
                                {format.description}
                              </SelectItem>
                            ))}
                          </SelectContent>
              
                        </Select>

              <button
                type="button"
                onClick={handleBack}
                className="text-sm text-blue-500 mt-2"
              >
                ← Back
              </button>
              <button
                type="button"
                onClick={handleBack}
                className="text-sm text-blue-500 mt-2"
              >
                Show Selected Format
              </button>
              
            </div>
          </FormCard>
        </div>
        <div className="w-[100vw] px-4 flex-shrink-0">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolores officiis cum voluptate amet fugiat sequi saepe maiores nulla veritatis eligendi odio ex autem minima similique dolorem maxime voluptates, natus error unde consequatur delectus laboriosam asperiores minus corrupti? Eveniet repellendus voluptate debitis delectus mollitia commodi inventore dolore modi at repudiandae saepe nisi aperiam, hic quos doloremque nam cupiditate earum maxime consectetur incidunt voluptatem? Nostrum eveniet commodi, atque animi, ex cum enim quae, magni dignissimos veniam fugiat assumenda? Laudantium totam assumenda, culpa eaque aperiam obcaecati pariatur ad enim suscipit voluptatum nisi? Voluptatem odio unde vel harum, modi voluptatibus ut ipsum nihil quia?
        </div>
      </div>
     </div>
    </>
  );
};

export default Assessment;
