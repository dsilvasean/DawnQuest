"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface SlidingFormProps {
  step: number;
  totalSteps: number;
  children: React.ReactNode;
  className?: string;
}

const SlidingForm = ({
  step,
  totalSteps,
  children,
  className,
}: SlidingFormProps) => {
  return (
    <motion.div
      initial={{ x: "100%", opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: "-100%", opacity: 0 }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
      className={cn("rounded-xl bg-background p-6 shadow-lg border", className)}
    >
              <div className="text-sm text-muted-foreground mb-4">Step {step} of {totalSteps}</div>
              {children}
    </motion.div>
    
  );
};

export default SlidingForm;
