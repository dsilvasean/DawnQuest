"use client";
import React, { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "react-toastify";
import Loader from "@/components/custom/Loader";
import FormCard from "@/components/custom/FormCard";
import { useRouter } from "next/navigation";

interface Grade { id: number; grade: string; }
interface Board { id: number; board_display: string; }

const Register = ()=>{
  const API_URL = process.env.NEXT_PUBLIC_API_URL
  const router = useRouter();

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [boards, setBoards] = useState<Board[]>([]);
  const [selectedBoard, setSelectedBoard] = useState("");
  const [grades, setGrades] = useState<Grade[]>([]);
  const [selectedGrade, setSelectedGrade] = useState("");

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API_URL}/grades`)
      .then(res => res.json())
      .then(data => setGrades(data));
    fetch(`${API_URL}/boards`)
      .then(res => res.json())
      .then(data => setBoards(data));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }

    const payload = {
      first_name: firstName,
      last_name: lastName,
      email,
      password,
      grade_id: parseInt(selectedGrade),
      board_id: parseInt(selectedBoard),
    };

    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/user/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      if (response.ok) {
        toast.success("User registered successfully redirecting to login page");
        const timer = setTimeout(()=>{
          router.push("/login");
        }, 3500)
        return;
      } else {
        toast.error(data.message);
      }
    } catch (error) {
      console.error("Error registering:", error);
    } finally {
      setLoading(false);
    }
  };

  return(
    <>
    <Loader loading={loading} fullScreen/>
    <FormCard title="Register Student" onSubmit={handleSubmit} loading={loading} buttonText="Register">
      <div className="grid gap-3">
        <Label>First Name</Label>
        <Input value={firstName} onChange={(e) => setFirstName(e.target.value)} placeholder="John" className="focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2" />
        <Label>Last Name</Label>
          <Input value={lastName} onChange={(e) => setLastName(e.target.value)} placeholder="Doe" className="focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2" />
          <Label>Email</Label>
          <Input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="john@gmail.com" className="focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2"/>
          <Label>Password</Label>
          <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2"/>
          <Label>Confirm Password</Label>
          <Input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2"/>
          <Label>Grade</Label>
          <Select value={selectedGrade} onValueChange={setSelectedGrade}>
            <SelectTrigger className="w-full"><SelectValue placeholder="Select Student Grade" /></SelectTrigger>
            <SelectContent>
              {grades.map(grade => (
                <SelectItem key={grade.id} value={grade.id.toString()}>
                  {grade.grade}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Label>Board</Label>
          <Select value={selectedBoard} onValueChange={setSelectedBoard}>
            <SelectTrigger className="w-full"><SelectValue placeholder="Select Board" /></SelectTrigger>
            <SelectContent>
              {boards.map(board => (
                <SelectItem key={board.id} value={board.id.toString()}>
                  {board.board_display}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
      </div>
    </FormCard>
    
    </>
  )


}

export default Register;