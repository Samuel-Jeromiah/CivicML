document.addEventListener('DOMContentLoaded', () => {
    const billListEl = document.getElementById('bill-list');
    const emptyStateEl = document.getElementById('empty-state');
    const selectedBillEl = document.getElementById('selected-bill');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultContainer = document.getElementById('result-container');
    const predictionResult = document.getElementById('prediction-result');
    const confidenceFill = document.getElementById('confidence-fill');
    const confidenceText = document.getElementById('confidence-text');
    const predictionCard = document.querySelector('.prediction-card');

    let currentBills = [];
    let selectedBill = null;

    // Load sample bills
    fetch('sample_bills.json')
        .then(res => res.json())
        .then(data => {
            currentBills = data;
            renderBillList();
        })
        .catch(err => {
            console.error('Error loading bills:', err);
            billListEl.innerHTML = '<div class="error" style="color:#ef4444; text-align:center; padding: 2rem;">Failed to load bills.</div>';
        });

    function renderBillList() {
        billListEl.innerHTML = '';
        currentBills.forEach((bill, index) => {
            const el = document.createElement('div');
            el.className = 'bill-item';
            el.dataset.index = index;
            el.innerHTML = `
                <div class="bill-item-header">
                    <span class="ld-badge">LD ${bill.id}</span>
                </div>
                <div class="bill-item-title">${bill.title}</div>
            `;
            el.addEventListener('click', () => selectBill(index, el));
            billListEl.appendChild(el);
        });
    }

    function selectBill(index, element) {
        // Update UI selection
        document.querySelectorAll('.bill-item').forEach(el => el.classList.remove('selected'));
        if (element) element.classList.add('selected');

        selectedBill = currentBills[index];

        // Hide empty state, show bill details
        emptyStateEl.classList.add('hidden');
        selectedBillEl.classList.remove('hidden');
        resultContainer.classList.add('hidden'); // hide previous result
        confidenceFill.style.width = '0%';

        // Populate text
        document.getElementById('bill-id').textContent = `LD ${selectedBill.id}`;
        document.getElementById('bill-title').textContent = selectedBill.title;
        document.getElementById('bill-text').textContent = selectedBill.text_snippet;
        document.getElementById('actual-committee').textContent = selectedBill.actual_committee;

        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = 'Analyze Bill <span class="icon">✨</span>';

        // Auto-analyze immediately to reduce clicks and scrolling
        analyzeSelectedBill();
    }

    async function analyzeSelectedBill() {
        if (!selectedBill) return;

        // UI Loading state
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = 'Analyzing... <span class="icon">⏳</span>';
        resultContainer.classList.add('hidden');

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text_embedding: selectedBill.embedding
                })
            });

            const data = await response.json();

            if (data.success) {
                showPrediction(data.data);
            } else {
                alert('Analysis failed: ' + data.error);
                analyzeBtn.disabled = false;
                analyzeBtn.innerHTML = 'Analyze Bill <span class="icon">✨</span>';
            }
        } catch (error) {
            console.error(error);
            alert('An error occurred during analysis.');
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = 'Analyze Bill <span class="icon">✨</span>';
        }
    }

    function showPrediction(result) {
        analyzeBtn.innerHTML = 'Analysis Complete <span class="icon">✅</span>';
        resultContainer.classList.remove('hidden');

        predictionResult.textContent = result.committee;

        // Calculate confidence percentage
        let conf = result.prediction ? result.probability : (1 - result.probability);
        let confPercent = Math.round(conf * 100);

        if (result.prediction) {
            predictionCard.classList.remove('is-other');
        } else {
            predictionCard.classList.add('is-other');
        }

        // Animate confidence bar
        setTimeout(() => {
            confidenceFill.style.width = confPercent + '%';
            confidenceText.textContent = confPercent + '%';
        }, 100);
    }
});
