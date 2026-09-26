<template>
  <div class="quiz-layout">
    <main class="quiz-content">
      <div class="header-section">
        <h2 class="title">Descubra seu Perfil de Investidor</h2>
        <p class="subtitle">Responda a um rápido questionário para descobrirmos a melhor estratégia para você.</p>
      </div>

      <div class="glass-card quiz-card result-card" v-if="alreadyCompleted && !retaking">
        <div class="result-icon">🎯</div>
        <h3 class="success-text">Você já possui um perfil mapeado!</h3>
        <p class="score-text">Perfil Atual: {{ translatedProfile }}</p>
        <p class="description-text">Você já descobriu sua estratégia ideal. Deseja refazer a avaliação ou voltar para o início?</p>
        
        <div class="result-actions">
          <button @click="retaking = true" class="premium-btn outline">Refazer Quiz</button>
          <button @click=".push('/')" class="premium-btn">Voltar para Dashboard</button>
        </div>
      </div>

      <div class="glass-card quiz-card" v-else-if="loading">
        <h3 class="loading-text">Carregando questionário...</h3>
      </div>

      <div class="glass-card quiz-card" v-else-if="questions.length > 0 && !finished">
        <div class="progress-indicator">
          Pergunta {{ currentIndex + 1 }} de {{ questions.length }}
        </div>
        
        <h3 class="question-text">{{ currentQuestion.question }}</h3>
        
        <div class="options-container">
          <button 
            v-for="(option, idx) in currentQuestion.options" 
            :key="idx"
            @click="selectOption(option.value)"
            class="option-btn premium-btn outline"
            :class="{ 'selected': answers[currentIndex] === option.value }"
          >
            {{ option.text }}
          </button>
        </div>

        <div class="navigation-actions">
          <button @click="prevQuestion" class="premium-btn outline sm-btn" :disabled="currentIndex === 0">Voltar</button>
          
          <button v-if="currentIndex < questions.length - 1" @click="nextQuestion" class="premium-btn sm-btn" :disabled="!answers[currentIndex]">Próxima</button>
          <button v-else @click="finishQuiz" class="premium-btn sm-btn" :disabled="!answers[currentIndex]">Concluir</button>
        </div>
      </div>
      
      <div class="glass-card quiz-card result-card" v-else-if="finished && resultData">
        <div class="result-icon">🎯</div>
        <h3 class="success-text">Perfil {{ resultData.profile_label }}</h3>
        <p class="score-text">Pontuação: {{ resultData.total_score }} / {{ resultData.max_score }}</p>
        <p class="description-text">{{ resultData.description }}</p>
        
        <div class="result-actions">
          <button @click="$router.push('/')" class="premium-btn">Voltar para Dashboard</button>
        </div>
      </div>
      
      <div class="glass-card quiz-card" v-else-if="finished && !resultData">
        <h3 class="loading-text">Avaliando suas respostas...</h3>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const questions = ref([]);
const alreadyCompleted = ref(false);
const retaking = ref(false);

const profileMap = {
  'CONSERVATIVE': 'Conservador',
  'MODERATE': 'Moderado',
  'AGGRESSIVE': 'Arrojado'
};
const translatedProfile = computed(() => {
  const p = authStore.user?.investor_profile;
  return profileMap[p] || p;
});
const answers = ref([]);
const currentIndex = ref(0);
const loading = ref(true);
const finished = ref(false);

const currentQuestion = computed(() => questions.value[currentIndex.value] || {});

const fetchQuestions = async () => {
  try {
    const res = await api.get('users/profile/quiz/questions/');
    questions.value = res.data.questions;
    answers.value = new Array(questions.value.length).fill(null);
  } catch (error) {
    console.error("Erro ao buscar questões:", error);
  } finally {
    loading.value = false;
  }
};

const selectOption = (val) => { answers.value[currentIndex.value] = val; };
const prevQuestion = () => { if (currentIndex.value > 0) currentIndex.value--; };
const nextQuestion = () => { if (currentIndex.value < questions.value.length - 1) currentIndex.value++; };

const resultData = ref(null);

const finishQuiz = async () => {
  finished.value = true;
  try {
    const payload = {
      answers: answers.value.map((val, idx) => ({ question_id: questions.value[idx].id, score: val }))
    };
    const res = await api.post('users/profile/quiz/evaluate/', payload);
    resultData.value = res.data;
    
    if (authStore.user) {
      authStore.user.investor_profile = res.data.profile;
    }
  } catch (error) {
    console.error("Erro ao avaliar quiz:", error);
    finished.value = false;
  }
};

onMounted(() => {
  if (authStore.user?.investor_profile) {
    alreadyCompleted.value = true;
  }
  fetchQuestions(); 
});
</script>

<style scoped>
.quiz-layout { display: flex; flex-direction: column; }
.quiz-content { flex: 1; padding: 40px; max-width: 800px; margin: 0 auto; width: 100%; }
.header-section { margin-bottom: 40px; text-align: center; }
.title { font-size: 2rem; font-weight: 600; margin-bottom: 8px; color: var(--gold-accent); }
.subtitle { color: var(--text-muted); font-size: 1.1rem; }
.quiz-card { padding: 40px !important; text-align: center; min-height: 400px; display: flex; flex-direction: column; justify-content: center; }
.progress-indicator { color: var(--gold-accent); font-weight: 600; margin-bottom: 20px; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
.question-text { font-size: 1.4rem; color: var(--text-main); margin-bottom: 30px; font-weight: 500; line-height: 1.4; }
.options-container { display: flex; flex-direction: column; gap: 16px; margin-bottom: 40px; }
.option-btn { width: 100%; text-align: left; padding: 16px 24px; font-size: 1.1rem; font-weight: 500; border-radius: 12px; transition: all 0.2s ease; background: #ffffff !important; color: #000000 !important; border: 1px solid #ffffff; }
.option-btn:hover { background: #b45309 !important; color: #ffffff !important; border-color: #b45309 !important; transform: translateY(-2px); }
.option-btn.selected { background: var(--gold-accent) !important; color: #000000 !important; border-color: var(--gold-accent) !important; font-weight: 600; transform: translateY(-2px); }
.navigation-actions { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-glass); padding-top: 24px; margin-top: auto; }
.sm-btn { padding: 10px 24px; width: auto; font-size: 1rem; }
.premium-btn:disabled { opacity: 0.3; cursor: not-allowed; transform: none; box-shadow: none; }
.success-text { color: var(--gold-accent); font-size: 1.5rem; }

.result-card { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.result-icon { font-size: 4rem; margin-bottom: 20px; }
.score-text { color: var(--text-muted); font-size: 1.2rem; margin-bottom: 20px; font-weight: 500; }
.description-text { color: var(--text-main); font-size: 1.1rem; line-height: 1.6; max-width: 600px; margin-bottom: 40px; margin-left: auto; margin-right: auto; }
.result-actions { display: flex; gap: 16px; justify-content: center; width: 100%; }

</style>
