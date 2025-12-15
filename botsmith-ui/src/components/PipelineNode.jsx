import { clsx } from 'clsx';
import { motion } from 'framer-motion';
import { Check, Circle, Loader2 } from 'lucide-react';
import { twMerge } from 'tailwind-merge';

export const PipelineNode = ({ step, status, isActive, label }) => {
    // status: pending, running, success, failed

    const isRunning = status === 'running';
    const isSuccess = status === 'success';
    const isFailed = status === 'failed';

    return (
        <div className="flex flex-col items-center relative z-10">
            <motion.div
                initial={{ scale: 0.8, opacity: 0.5 }}
                animate={{
                    scale: isActive || isRunning ? 1.1 : 1,
                    opacity: 1,
                    borderColor: isRunning ? '#00E1FF' : isSuccess ? '#19F5A0' : isFailed ? '#FF4F6D' : '#334155',
                    boxShadow: isRunning ? '0 0 15px rgba(0, 225, 255, 0.6)' : 'none'
                }}
                className={twMerge(
                    "w-12 h-12 rounded-full border-2 flex items-center justify-center bg-background transition-colors duration-300",
                    "relative"
                )}
            >
                {isRunning && (
                    <motion.div
                        className="absolute inset-0 rounded-full border-2 border-glow opacity-50"
                        animate={{ scale: [1, 1.5], opacity: [0.5, 0] }}
                        transition={{ repeat: Infinity, duration: 1.5 }}
                    />
                )}

                {isRunning ? (
                    <Loader2 className="w-5 h-5 text-glow animate-spin" />
                ) : isSuccess ? (
                    <Check className="w-6 h-6 text-success" />
                ) : isFailed ? (
                    <span className="text-failure font-bold">!</span>
                ) : (
                    <Circle className="w-4 h-4 text-gray-600" />
                )}
            </motion.div>

            <motion.span
                className={clsx(
                    "mt-2 text-xs font-medium uppercase tracking-wider",
                    isRunning ? "text-glow" : isSuccess ? "text-success" : "text-gray-500"
                )}
            >
                {label}
            </motion.span>
        </div>
    );
};
