"use client";

import React, { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { useRouter } from "next/navigation";
import { ArrowBigLeft } from "lucide-react";

import FormCard from "@/components/custom/FormCard";
import { MultiSelect } from "@/components/custom/multi-select";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  fetchChapters,
  fetchPatterns,
  fetchSubjects,
  fetchUserProfile,
  generateAssessment,
} from "@/lib/api";
import type { Student, Subject, PaperFormat, Chapter } from "@/types/student";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const Assessment = () => {
  const router = useRouter();

  type Step = 1 | 2 | 3;

  const [step, setStep] = useState<Step>(1);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [student, setStudent] = useState<Student>();
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [paperFormat, setPaperFormat] = useState<PaperFormat[]>([]);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [chapterOptions, setChapterOptions] = useState<{ label: string; value: string }[]>([]);
  const [chapter_count, setChapterCount] = useState<number>();

  // form data
  const [selectedSubject, setSelectedSubject] = useState<Subject>();
  const [selectedPaperFormat, setSelectedPaperFormat] = useState<PaperFormat>();
  const [selectedChapters, setSelectedChapters] = useState<string[]>([]);

  useEffect(() => {
    const tokenFromStorage = localStorage.getItem("access_token");
    if (!tokenFromStorage) {
      setLoading(true);
      toast.error("Unauthorized");
      setTimeout(() => router.push("/login"), 3000);
    } else {
      console.log(tokenFromStorage);
      setToken(tokenFromStorage);
    }
  }, []);

  useEffect(() => {
    if (!token) return;

    fetchUserProfile(token).then((data) => {
      const StudentObj: Student = {
        name: "Hello",
        email: data.data.email,
        grade: data.data.grade.grade,
        board: data.data.board.id,
        board_display: data.data.board.board_display,
      };
      setStudent(StudentObj);
    });
  }, [token]);

  useEffect(() => {
    if (student?.board && student?.grade) {
      fetchSubjects(student.board, student.grade).then((data) => {
        setSubjects(data);
      });
    }
  }, [student]);

  useEffect(() => {
    if (selectedSubject) {
      fetchChapters(selectedSubject.id).then((data) => {
        setChapters(data);
        const options = data.map((chapter: Chapter) => ({
          label: chapter.name,
          value: chapter.id,
        }));
        setChapterOptions(options);

        console.log(data);
      });
    }
  }, [selectedPaperFormat, selectedSubject]);

  const handleNext = async (e: React.FormEvent, next_step: Step) => {
    e.preventDefault();
    console.log(next_step);
    if (!selectedSubject) {
      toast.error("Please select a subject first");
      return;
    }
    if (student?.grade && token) {
      fetchPatterns(selectedSubject.id, student?.grade, token).then((data) => {
        console.log("patterns fetched");
        setPaperFormat(data);
        console.log(paperFormat);
        setStep(next_step);
      });
    }
  };

  const handleBack = async (e: React.FormEvent, prev_step: Step) => {
    e.preventDefault();
    console.log(prev_step);
    setStep(prev_step);
  };

  const handleSubmit = async (e:React.FormEvent)=>{
    e.preventDefault()
    generateAssessment(selectedPaperFormat?.id ?? 0, selectedChapters, token?? "").then((data)=>{
      toast.success("Assesment Generated Successfully");
      console.log(data)
      router.push(`/dashboard/assessment/${data.data.meta.assessment_id}`)
    })

  }

  return (
    <>
      <div className="relative overflow-hidden w-full">
        <div
          className="flex transition-transform duration-500"
          style={{ transform: `translateX(-${(step - 1) * 100}vw)` }}
        >
          <div className="w-[100vw] px-4 flex-shrink-0">
            {/* Step 1 */}
            <FormCard
              title="Assessment"
              onSubmit={(e) => handleNext(e, 2)}
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
                <Select
                  value={selectedSubject?.name}
                  onValueChange={(value) => {
                    const selectedSub = subjects.find((subject) => {
                      return subject.name === value;
                    });
                    setSelectedSubject(selectedSub);
                  }}
                >
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
            {/* Step 2 */}
            <FormCard
              title="Select Paper Format"
              onSubmit={(e) => {
                e.preventDefault();
                setStep(3);
              }}
              loading={loading}
              buttonText="Submit"
            >
              <div className="grid gap-3">
                <Label>Paper Format</Label>
                <Select
                  value={selectedPaperFormat?.description}
                  onValueChange={(val) => {
                    const selectedPaperForm = paperFormat.find((format_) => {
                      return format_.description === val;
                    });
                    setSelectedPaperFormat(selectedPaperForm);
                    setChapterCount(selectedPaperForm?.chapter_count);
                  }}
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Select Paper Format" />
                  </SelectTrigger>

                  <SelectContent>
                    {paperFormat.map((format) => (
                      <SelectItem
                        key={format.id}
                        value={format.description.toString()}
                      >
                        {format.description}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <div className="flex justify-center mt-4">
                  <button
                    type="button"
                    onClick={(e) => handleBack(e, 1)}
                    className="text-sm text-brand flex items-center space-x-1"
                  >
                    <ArrowBigLeft />
                  </button>
                </div>
              </div>
            </FormCard>
          </div>

          <div className="w-[100vw] px-4 flex-shrink-0">
            {/* Part 3 */}
            <FormCard
              title="Select Chapters"
              onSubmit={handleSubmit}
              loading={loading}
              buttonText="Submit"
            >
              <div className="grid gap-3">
                <Label>Select {`${chapter_count} Chapters`}</Label>

                <MultiSelect
                asChild={true}
                options={chapterOptions.map((opt) => ({
                  ...opt,
                  disabled: chapter_count !== undefined &&
                            selectedChapters.length >= chapter_count &&
                            !selectedChapters.includes(opt.value),
                }))}
                  onValueChange={(val) => {
                    if (chapter_count && val.length <= chapter_count) {
                      setSelectedChapters(val);
                    } else {
                      toast.error(
                        `You can select upto ${chapter_count} chapters only`
                      );
                    }
                  }}
                  defaultValue={selectedChapters}
                  placeholder="Select Chapters"
                  variant="secondary"
                  maxCount={2}
                  className="flex flex-wrap gap-1 max-w-full"
                />
                <div className="mt-4">
                  <h2 className="text-xl font-semibold">Selected Chapters:</h2>
                  <ul className="list-disc list-inside">
                    {selectedChapters.map((chapter) => (
                      <li key={chapter}>{chapter}</li>
                    ))}
                  </ul>
                </div>
              </div>
              <button
                type="button"
                onClick={(e) => handleBack(e, 2)}
                className="text-sm text-brand flex items-center space-x-1"
              >
                <ArrowBigLeft />
              </button>
            </FormCard>
          </div>
        </div>
      </div>
    </>
  );
};

export default Assessment;
