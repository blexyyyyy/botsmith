import { AnimatePresence, motion } from 'framer-motion';
import { FileCode, FolderOpen } from 'lucide-react';

export const FileTree = ({ files }) => {
    return (
        <div className="h-full flex flex-col">
            <div className="flex items-center gap-2 px-4 py-2 border-b border-gray-800 bg-gray-900/50 backdrop-blur">
                <FolderOpen size={16} className="text-secondaryGlow" />
                <span className="text-sm font-mono font-bold text-gray-400">GENERATED FILES</span>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-1">
                <AnimatePresence>
                    {files.map((file, i) => (
                        <motion.div
                            key={file.filename || i}
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            className="flex items-center gap-2 p-2 hover:bg-white/5 rounded cursor-pointer group"
                        >
                            <FileCode size={16} className="text-blue-400 group-hover:text-glow transition-colors" />
                            <span className="text-sm text-gray-300 group-hover:text-white transition-colors">
                                {file.filename}
                            </span>
                            {file.size && (
                                <span className="text-xs text-gray-600 ml-auto">{file.size}b</span>
                            )}
                        </motion.div>
                    ))}
                </AnimatePresence>

                {files.length === 0 && (
                    <div className="text-center text-gray-600 mt-10 italic">
                        Waiting for generation...
                    </div>
                )}
            </div>
        </div>
    );
};
