import './DashboardCards.css';

function DashboardCard({ title, extraClasses, children }) {
    return (
        <div className={`card ${extraClasses}`}>
            <h1>{title}</h1>
            <div className='flex-col' style={{ width: '100%', overflowY: 'scroll', gap: '5px', alignItems: 'center' }}>{children}</div>
        </div>
    );
}

function DashboardCardTitleless({ extraClasses, children }) {
    return (
        <div className={`card2 ${extraClasses}`}>
            {children}
        </div>
    );
}

export { DashboardCard, DashboardCardTitleless };