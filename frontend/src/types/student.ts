export interface Student {
    name: string;
    grade: number;
    board: number;
    board_display: string;
    email: string;
  }
  
  export interface Subject {
    id: number;
    name: string;
  }
  
  export interface PaperFormat {
    id: number;
    description: string;
    chapter_count:number
  }

  export interface Chapter {
    id: number;
    name: string;
  }

