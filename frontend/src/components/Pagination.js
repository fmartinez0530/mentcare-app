import React from 'react';
// import classnames from 'classnames';
import './Pagination.css';
import '../pages/styles/PatientDashboard.css'

const Pagination = (props) => {
    const {
        onPageChange,
        totalCount,
        currentPage,
        pageSize,
        className,
    } = props;

    const PaginationButtons = [];
    const lastPage = Math.ceil(totalCount / pageSize);
    if (currentPage === 1 && currentPage !== lastPage) {
        PaginationButtons.push(
            <button
                key={`pagination-item-${currentPage}`} // unique key
                // className={classnames('pagination-item', {
                //     selected: (i + 1) === currentPage
                // })}
                className={className}
                onClick={() => onPageChange(2)}
            >
                {'NEXT'}
            </button>
        );
    }
    else if (currentPage > 1 && currentPage !== lastPage) {
        PaginationButtons.push(
            <button
                key={`pagination-item-back`} // unique key
                // className={classnames('pagination-item', {
                //     selected: (i + 1) === currentPage
                // })}
                className={className}
                onClick={() => onPageChange(currentPage - 1)}
            >
                {'BACK'}
            </button>
        );
        PaginationButtons.push(
            <button
                key={`pagination-item-next`} // unique key
                // className={classnames('pagination-item', {
                //     selected: (i + 1) === currentPage
                // })}
                className={className}
                onClick={() => onPageChange(currentPage + 1)}
            >
                {'NEXT'}
            </button>
        );
    }
    else if (currentPage > 1 && currentPage === lastPage) {
        PaginationButtons.push(
            <button
                key={`pagination-item-back`} // unique key
                // className={classnames('pagination-item', {
                //     selected: (i + 1) === currentPage
                // })}
                className={className}
                onClick={() => onPageChange(currentPage - 1)}
            >
                {'BACK'}
            </button>
        );
    }

    return (
        (PaginationButtons.map((button) => button))
    );
};

export default Pagination;
