import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { submitApplication } from '../api/career'
import '../styles/Apply.css'

/* ---- Icon Set ---- */
const IconUpload = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="16 16 12 12 8 16" />
        <line x1="12" y1="12" x2="12" y2="21" />
        <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3" />
    </svg>
)

const IconUser = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" />
    </svg>
)

const IconClipboard = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
        <rect x="8" y="2" width="8" height="4" rx="1" />
    </svg>
)

const IconFolder = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
    </svg>
)

const IconBriefcase = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="7" width="20" height="14" rx="2" />
        <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2" />
    </svg>
)

const IconGradCap = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="12 2 22 8.5 12 15 2 8.5 12 2" />
        <polyline points="6 11.5 6 18 12 21 18 18 18 11.5" />
    </svg>
)

const IconLeaf = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z" />
        <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12" />
    </svg>
)

const IconCheck = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="20 6 9 17 4 12" />
    </svg>
)

const IconX = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
    </svg>
)

const IconLock = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="11" width="18" height="11" rx="2" />
        <path d="M7 11V7a5 5 0 0 1 10 0v4" />
    </svg>
)

const IconArrow = () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
        <line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" />
    </svg>
)

/* ---- App Types ---- */
const APP_TYPES = [
    { key: 'job', label: 'Full-Time Job', Icon: IconBriefcase, activeClass: 'active-job' },
    { key: 'fellowship', label: 'Fellowship', Icon: IconGradCap, activeClass: 'active-fellowship' },
    { key: 'internship', label: 'Internship', Icon: IconLeaf, activeClass: 'active-internship' },
]

const FELLOWSHIP_PROGRAMS = ['Agri Research', 'Field Innovation', 'Data Analytics', 'Climate Adaptation', 'Rural Economics']
const INTERNSHIP_TYPES = ['Technical', 'Field Operations', 'Marketing', 'Research', 'Finance']

/* ---- File Upload Component ---- */
function FileUpload({ id, label, name, onChange, required }) {
    const [fileName, setFileName] = useState('')
    const handleChange = (e) => {
        const file = e.target.files[0]
        if (file) { setFileName(file.name); onChange(name, file) }
    }
    return (
        <div className="form-group">
            <label className="form-label" htmlFor={id}>
                {label}{required && <span className="req"> *</span>}
            </label>
            <div className="file-upload-zone">
                <input type="file" id={id} accept=".pdf,.png,.jpg,.jpeg" onChange={handleChange} />
                <div className="file-upload-zone__icon"><IconUpload /></div>
                <div className="file-upload-zone__title">Click to upload or drag and drop</div>
                <div className="file-upload-zone__hint">PDF, PNG, JPG — max 5 MB</div>
                {fileName && (
                    <div className="file-upload-zone__name">
                        <IconCheck /> {fileName}
                    </div>
                )}
            </div>
        </div>
    )
}

/* ---- Main Component ---- */
export default function Apply() {
    const [searchParams] = useSearchParams()
    const [appType, setAppType] = useState(searchParams.get('type') || 'job')
    const [loading, setLoading] = useState(false)
    const [status, setStatus] = useState(null)

    const [fields, setFields] = useState({
        full_name: '', email: '', phone: '', city: '', state: '', country: 'India',
        education: '', experience: '', internship_type: '', fellowship_program: '',
        linkedin: '', portfolio: '', reason: '', skills: '',
    })
    const [files, setFiles] = useState({ resume: null, id_proof: null, certificates: null })

    useEffect(() => {
        const t = searchParams.get('type')
        if (t) setAppType(t)
        window.scrollTo(0, 0)
    }, [searchParams])

    const handleField = (e) => setFields(prev => ({ ...prev, [e.target.name]: e.target.value }))
    const handleFile = (name, file) => setFiles(prev => ({ ...prev, [name]: file }))

    const handleSubmit = async (e) => {
        e.preventDefault()
        setStatus(null)
        setLoading(true)
        try {
            const formData = new FormData()
            formData.append('application_type', appType)
            Object.entries(fields).forEach(([k, v]) => formData.append(k, v))
            if (files.resume) formData.append('resume', files.resume)
            if (files.id_proof) formData.append('id_proof', files.id_proof)
            if (files.certificates) formData.append('certificates', files.certificates)

            await submitApplication(formData)
            setStatus({ type: 'success', msg: 'Application submitted successfully! We will reach out within 3-5 business days.' })
            setFields({ full_name: '', email: '', phone: '', city: '', state: '', country: 'India', education: '', experience: '', internship_type: '', fellowship_program: '', linkedin: '', portfolio: '', reason: '', skills: '' })
            setFiles({ resume: null, id_proof: null, certificates: null })
        } catch (err) {
            setStatus({ type: 'error', msg: err.message })
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="apply-page">
            <div className="container">

                <div className="page-hero">
                    <div className="section-label" style={{ justifyContent: 'center' }}>Step Into AgriFabrix</div>
                    <h1 className="page-hero__title">Submit Your Application</h1>
                    <p className="page-hero__desc">Choose an opportunity type and complete the form below.</p>
                </div>

                {/* Type Selector */}
                <div className="type-tabs">
                    {APP_TYPES.map(({ key, label, Icon, activeClass }) => (
                        <button
                            key={key}
                            id={`tab-${key}`}
                            type="button"
                            className={`type-tab ${appType === key ? activeClass : ''}`}
                            onClick={() => { setAppType(key); setStatus(null) }}
                        >
                            <Icon /> {label}
                        </button>
                    ))}
                </div>

                {/* Alert */}
                {status && (
                    <div className={`alert alert-${status.type}`} style={{ maxWidth: 500, margin: '0 auto 20px' }}>
                        {status.type === 'success' ? <IconCheck /> : <IconX />}
                        {status.msg}
                    </div>
                )}

                <form onSubmit={handleSubmit} noValidate>
                    <div className="form-card">

                        {/* Personal Info */}
                        <div className="form-section-title">
                            <IconUser /> Personal Information
                        </div>
                        <div className="form-grid">
                            <div className="form-group">
                                <label className="form-label" htmlFor="full_name">Full Name<span className="req"> *</span></label>
                                <input id="full_name" name="full_name" className="form-input" placeholder="e.g. Ravi Kumar" value={fields.full_name} onChange={handleField} required />
                            </div>
                            <div className="form-group">
                                <label className="form-label" htmlFor="email">Email Address<span className="req"> *</span></label>
                                <input id="email" name="email" type="email" className="form-input" placeholder="you@example.com" value={fields.email} onChange={handleField} required />
                            </div>
                            <div className="form-group">
                                <label className="form-label" htmlFor="phone">Phone Number<span className="req"> *</span></label>
                                <input id="phone" name="phone" className="form-input" placeholder="+91 9XXXXXXXXX" value={fields.phone} onChange={handleField} required />
                            </div>
                            <div className="form-group">
                                <label className="form-label" htmlFor="city">City</label>
                                <input id="city" name="city" className="form-input" placeholder="e.g. Hyderabad" value={fields.city} onChange={handleField} />
                            </div>
                            <div className="form-group">
                                <label className="form-label" htmlFor="state">State</label>
                                <input id="state" name="state" className="form-input" placeholder="e.g. Telangana" value={fields.state} onChange={handleField} />
                            </div>
                            <div className="form-group">
                                <label className="form-label" htmlFor="country">Country</label>
                                <input id="country" name="country" className="form-input" placeholder="India" value={fields.country} onChange={handleField} />
                            </div>
                        </div>

                        {/* Professional Info */}
                        <div className="form-section-title" style={{ marginTop: 8 }}>
                            <IconClipboard /> Professional Details
                        </div>
                        <div className="form-grid">
                            <div className="form-group">
                                <label className="form-label" htmlFor="education">Education</label>
                                <input id="education" name="education" className="form-input" placeholder="e.g. B.Sc Agriculture, IIT" value={fields.education} onChange={handleField} />
                            </div>
                            <div className="form-group">
                                <label className="form-label" htmlFor="experience">Work Experience</label>
                                <input id="experience" name="experience" className="form-input" placeholder="e.g. 3 years in field operations" value={fields.experience} onChange={handleField} />
                            </div>

                            {appType === 'fellowship' && (
                                <div className="form-group">
                                    <label className="form-label" htmlFor="fellowship_program">Fellowship Program</label>
                                    <select id="fellowship_program" name="fellowship_program" className="form-select" value={fields.fellowship_program} onChange={handleField}>
                                        <option value="">Select a program</option>
                                        {FELLOWSHIP_PROGRAMS.map(p => <option key={p} value={p}>{p}</option>)}
                                    </select>
                                </div>
                            )}

                            {appType === 'internship' && (
                                <div className="form-group">
                                    <label className="form-label" htmlFor="internship_type">Internship Type</label>
                                    <select id="internship_type" name="internship_type" className="form-select" value={fields.internship_type} onChange={handleField}>
                                        <option value="">Select type</option>
                                        {INTERNSHIP_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
                                    </select>
                                </div>
                            )}

                            <div className="form-group">
                                <label className="form-label" htmlFor="linkedin">LinkedIn Profile</label>
                                <input id="linkedin" name="linkedin" className="form-input" placeholder="https://linkedin.com/in/yourname" value={fields.linkedin} onChange={handleField} />
                            </div>
                            <div className="form-group">
                                <label className="form-label" htmlFor="portfolio">Portfolio / Website</label>
                                <input id="portfolio" name="portfolio" className="form-input" placeholder="https://yourwebsite.com" value={fields.portfolio} onChange={handleField} />
                            </div>
                        </div>

                        <div className="form-grid form-grid--1">
                            <div className="form-group">
                                <label className="form-label" htmlFor="skills">Key Skills</label>
                                <input id="skills" name="skills" className="form-input" placeholder="e.g. Python, Data Analysis, Farm Management" value={fields.skills} onChange={handleField} />
                            </div>
                            <div className="form-group">
                                <label className="form-label" htmlFor="reason">Why AgriFabrix?<span className="req"> *</span></label>
                                <textarea id="reason" name="reason" className="form-textarea" rows={4} placeholder="Tell us why you want to join and what you will bring to the team..." value={fields.reason} onChange={handleField} required />
                            </div>
                        </div>

                        {/* Documents */}
                        <div className="form-section-title" style={{ marginTop: 8 }}>
                            <IconFolder /> Upload Documents
                        </div>
                        <div className="form-grid">
                            <FileUpload id="file-resume" label="Resume / CV" name="resume" onChange={handleFile} required />
                            <FileUpload id="file-id-proof" label="ID Proof" name="id_proof" onChange={handleFile} />
                            <FileUpload id="file-certificates" label="Certificates / Transcripts" name="certificates" onChange={handleFile} />
                        </div>

                        {/* Footer */}
                        <div className="form-footer">
                            <p className="form-note">
                                <IconLock /> Your data is secure. We never share personal information.
                            </p>
                            <button
                                id="submit-application-btn"
                                type="submit"
                                className="btn btn-primary btn-lg"
                                disabled={loading}
                                style={{ opacity: loading ? 0.7 : 1 }}
                            >
                                {loading ? <><span className="spinner" /> Submitting</> : <>Submit Application <IconArrow /></>}
                            </button>
                        </div>

                    </div>
                </form>
            </div>
        </div>
    )
}
