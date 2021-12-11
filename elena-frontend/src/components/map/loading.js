import './loading.css'

export default function Loading() {
    return (
        <div className="loading-wrap">
            <svg className="loading" viewBox="25 25 50 50">
                <circle cx="50" cy="50" r="20"></circle>
            </svg>
        </div>
    )
}