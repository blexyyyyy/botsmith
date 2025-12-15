export const createEventSource = (prompt, projectName, onEvent) => {
    console.log("Creating EventSource connection...");
    // Reverting to localhost as it matches the successful Python E2E test
    const url = `http://localhost:8000/bot/stream?prompt=${encodeURIComponent(prompt)}&project_name=${encodeURIComponent(projectName)}`;
    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            onEvent(data);

            if (data.type === 'done') {
                eventSource.close();
            }
        } catch (e) {
            console.error("Failed to parse SSE message", e);
        }
    };

    eventSource.onerror = (err) => {
        console.error("SSE Error", err);
        eventSource.close();
        onEvent({ type: 'error', data: { message: "Connection lost" } });
    };

    return eventSource;
};
