const API_BASE_URL = "https://admin.agrifabrix.in/api/static";

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

export const sendOTP = async (email) => {
    try {
        const response = await fetch(`${API_BASE_URL}/Career/SendOTP`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to send OTP');
        }

        return data;
    } catch (error) {
        console.error("Error sending OTP:", error);
        throw error;
    }
};

export const verifyOTP = async (email, otp) => {
    try {
        const response = await fetch(`${API_BASE_URL}/Career/VerifyOTP`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, otp }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Verification failed');
        }

        return data;
    } catch (error) {
        console.error("Error verifying OTP:", error);
        throw error;
    }
};
