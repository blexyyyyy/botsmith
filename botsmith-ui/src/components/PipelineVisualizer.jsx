import { motion } from 'framer-motion';
import { PipelineNode } from './PipelineNode';

// Standard BotSmith workflow steps
const WORKFLOW_STEPS = [
    "scaffold_project",
    "plan_files",
    "define_agents",
    "configure_agents",
    "design_api",
    "implement_api",
    "generate_all_files",
    "validate_code",
    "security_scan",
    "optimize_workflow",
    "deployment"
];

export const PipelineVisualizer = ({ currentStep, stepsStatus }) => {
    return (
        <div className="w-full py-8 overflow-x-auto relative">
            {/* Connecting Line - Background */}
            <div className="absolute top-14 left-0 w-full h-1 bg-gray-800 z-0" />

            {/* Active Beam Animation */}
            <motion.div
                className="absolute top-14 left-0 h-1 bg-gradient-to-r from-transparent via-glow to-transparent z-0 opacity-50"
                animate={{ x: ["-100%", "100%"] }}
                transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
            />

            <div className="flex justify-between min-w-max px-8 gap-8">
                {WORKFLOW_STEPS.map((stepKey, index) => {
                    // Normalize step key to readable label
                    const label = stepKey.replace(/_/g, " ");
                    const status = stepsStatus[stepKey] || (currentStep === stepKey ? 'running' : 'pending');
                    const isActive = currentStep === stepKey;

                    return (
                        <PipelineNode
                            key={stepKey}
                            step={stepKey}
                            label={label}
                            status={status}
                            isActive={isActive}
                        />
                    );
                })}
            </div>
        </div>
    );
};
