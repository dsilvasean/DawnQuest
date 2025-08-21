// lib/generatePDF.ts

// Use CommonJS-style import for compatibility in Next.js client code
const pdfMake = require("pdfmake/build/pdfmake");
const pdfFonts = require("pdfmake/build/vfs_fonts");

// Register the fonts correctly (pdfFonts.vfs is the correct object)
pdfMake.vfs = pdfFonts.pdfMake ? pdfFonts.pdfMake.vfs : pdfFonts.vfs;

export const generateAssessmentPdf = (assessment: any) => {
  const questions = assessment.data?.raw_json;

  const content: any[] = [
    { text: 'Assessment Preview', style: 'header' },
    { text: `ID: ${assessment.data.id}`, margin: [0, 0, 0, 10] },
  ];

  // Function to safely strip HTML tags from strings
  function stripHtml(html: string): string {
    return html ? html.replace(/<[^>]+>/g, '') : '';
  }

  // Render a question safely with checks for the 'data' property
  const renderQuestion = (q: any, index: number) => {
    const questionContent: string[] = [];
  
    if (Array.isArray(q.data) && q.data.length > 0) {
      // Usual case: question with data array
      q.data.forEach((item: any) => {
        if (item.content) questionContent.push(stripHtml(item.content));
      });
    } else if (typeof q.content === "string" && q.content.trim() !== "") {
      // Fallback if question content is a direct string
      questionContent.push(stripHtml(q.content));
    } else {
      // No content found
      questionContent.push("No question data available");
    }
  
    return {
      margin: [0, 5, 0, 10],
      stack: [
        { text: `Q${index + 1}:`, bold: true },
        ...questionContent.map(text => ({ margin: [10, 2, 0, 2], text })),
      ],
    };
  };
  
  if (!questions || typeof questions !== 'object') {
    content.push({ text: 'No questions available or invalid format.' });
  } else {
    Object.keys(questions).forEach((key, index) => {
      const q = questions[key];
      console.log(`Rendering question ${index + 1}`, q); // Debug log

      if (!q.has_subquestions) {
        content.push(renderQuestion(q, index));
      } else {
        content.push({ text: `Q${index + 1}: (with subquestions)`, bold: true });
        if (Array.isArray(q.data)) {
          q.data.forEach((subq: any, subIndex: number) => {
            content.push({
              margin: [10, 2, 0, 2],
              text: `Subquestion ${stripHtml(subq.content || '')} (${subq.marks} marks)`
            });

            if (Array.isArray(subq.data)) {
              subq.data.forEach((item: any) => {
                content.push({
                  margin: [20, 2, 0, 2],
                  text: stripHtml(item.content || '')
                });
              });
            } else {
              content.push({ text: 'No subquestion data available' });
            }
          });
        } else {
          content.push({ text: 'No subquestions data available' });
        }
      }
    });
  }

  const docDefinition = {
    content,
    styles: {
      header: {
        fontSize: 20,
        bold: true,
        margin: [0, 0, 0, 10],
      },
    },
  };

  pdfMake.createPdf(docDefinition).download(`Assessment-${assessment.data.id}.pdf`);
};
