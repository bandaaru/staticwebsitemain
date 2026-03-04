const API_BASE_URL = "http://localhost:5000/api/static"; // Update this to production URL when deploying

export const submitApplication = async (formData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/Career/Apply`, {
            method: 'POST',
            body: formData, // FormData doesn't need Content-Type header for multipart
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to submit application');
        }

        return data;
    } catch (error) {
        console.error("Error submitting application:", error);
        throw error;
    }
};
