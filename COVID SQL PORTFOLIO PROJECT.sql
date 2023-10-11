select *
from CovidDeaths
order by 3,4

select *
from CovidVaccinations
order by 3,4

select location, date, total_cases, new_cases, total_deaths, population
from CovidDeaths
order by 1, 2

---LOOKING AT PERCENTAGE OF TOTAL DEATHS PER CASES

select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS death_percentage
from CovidDeaths
order by 1, 2

---LOOKING AT PERCENTAGE OF TOTAL DEATHS PER CASES IN UNITED STATES
---DEATH RATE PEAKED IN THE U.S. AT JUST OVER 6% IN MAY OF 2020, AND DROPPED TO JUST UNDER 2% THE FOLLOWING YEAR WITH THE LOWEST RECORD OF 1.68% IN JANUARY OF 2021

select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS death_percentage
from CovidDeaths
where location like '%States%'
order by 1, 2

---WE CAN SEE THAT EVEN AS THE DEATH RATE REDUCED, THE INFECTION RATE CONTINUED TO INCREASE STEADILY IN THE U.S.
select location, date, population, total_cases, total_deaths, (total_deaths/total_cases)*100 AS death_percentage, (total_cases/population)*100 AS infection_rate
from CovidDeaths
where location like '%States%'
order by 1, 2


---COUNTRIES WITH HIGHEST INFECTION RATE COMPARED TO POPULATION
---WE CAN SEE THAT DURING THE PANDEMIC ANDORRA ALTHOUGH A COUNTRY WITH ONE OF THE SMALLEST POPULATIONS HAS THE THE HIGHEST RATE OF INFECTION. 
---ALSO IT IS CLEARL TO SEE THAT COUNTRIES WITH REALLY SMALL POPULATIONS HAD QUITE ONE OF THE HIGHEST INFECTION RATES
select location, population,  max (total_cases) as highest_infections_count_per_country, max (total_cases/population)*100 AS highest_infection_rate
from CovidDeaths
group by location, population
order by 4 desc

---COUNTRIES WITH THE HIGHEST DEATH COUNT 
select location, max (total_deaths) total_death_count
from CovidDeaths
where continent is not null
group by location
order by 2 desc

---SHOWING THE CONTINENTS WITH THE HIGHEST DEATH COUNTS
select continent,max(total_deaths) as total_death_counts
from CovidDeaths
where continent is not null
group by continent
order by 2 desc

---SHOWING TOTAL GLOBAL DEATH PERCENTAGES OVERTIME

select date, sum (new_cases ) as total_cases, sum(new_deaths) as total_deaths, sum(new_deaths)/sum(new_cases)*100 as global_death_percentages
from CovidDeaths
where continent is not null
group by date
order by 1,2

---SHOWING OVERALL, ALL TIME TOTAL GLOBAL DEATH PERCENTAGES
select sum (new_cases ) as total_cases, sum(new_deaths) as total_deaths, sum(new_deaths)/sum(new_cases)*100 as global_death_percentages
from CovidDeaths
where continent is not null
order by 1,2

---VIEWING THE SECOND TABLE (COVID VACCINATION TABLE) AND JOINING WITH FIRST TABLE (COVID DEATHS)
select *
from CovidDeaths dea
join CovidVaccinations vac
     on dea.location = vac.location
	 and dea.date = vac.date

---LOOKING AT POPULATION VS NEW VACCINATIONS EVERYDAY
select dea.continent, dea.location, dea.date, dea.population, new_vaccinations
from CovidDeaths dea
join CovidVaccinations vac
     on dea.date = vac.date
	 and dea.location = vac.location
	 where dea.continent is not null
order by 2,3

---LOOKING AT SUM OF NEW VACCINATIONS EACH DAY BY LOCATION

select dea.continent, dea.location, dea.date, dea.population, new_vaccinations, sum (new_vaccinations) over (partition by dea.location order by dea.date ) as rolling_vaccination_sum
from CovidDeaths dea
join CovidVaccinations vac
     on dea.location = vac.location
	 and dea.date = vac.date
where dea.continent is not null
order by 2,3

---VIEWING THE PERCENTAGE OF THE VACCINATED POPULATION FOR EACH DAY WE MUST INTRODUCE CTE TO CALCULATE THE NEWLY CREATED TABLE
with popvac
as
(
select dea.continent, dea.location, dea.date, dea.population, new_vaccinations, sum (new_vaccinations) over (partition by dea.location order by dea.date ) as rolling_vaccination_sum
from CovidDeaths dea
join CovidVaccinations vac
     on dea.location = vac.location
	 and dea.date = vac.date
where dea.continent is not null
)
select *, (rolling_vaccination_sum/population)*100  daily_vacc_percentage
from popvac

---OR ALTERNATIVELY USING A TEMPORARY TABLE TO ACHIEVE THE SAME RESULT

create table #population_vacc_percentage
(
continent nvarchar(225),
location nvarchar(225),
date datetime,
population numeric,
New_vaccinations numeric,
rolling_vaccination_sums numeric
)
insert into #population_vacc_percentage
select dea.continent, dea.location, dea.date, dea.population, new_vaccinations, sum (new_vaccinations) over (partition by dea.location order by dea.date ) as rolling_vaccination_sum
from CovidDeaths dea
join CovidVaccinations vac
     on dea.location = vac.location
	 and dea.date = vac.date
where dea.continent is not null

select *, (rolling_vaccination_sums/population)*100
from #population_vacc_percentage

---CREATING A VIEW TABLE WITH ONE OF THE PAST QUERRIES FOR POSSIBLE POWERBI OR TABLEU VISUALIZATION
create view population_vaccinated as
select dea.continent, dea.location, dea.date, dea.population, new_vaccinations, sum (new_vaccinations) over (partition by dea.location order by dea.date ) as rolling_vaccination_sum
from CovidDeaths dea
join CovidVaccinations vac
     on dea.location = vac.location
	 and dea.date = vac.date
where dea.continent is not null

---VIEWING THE CREATED VIEW TABLE
select *
from population_vaccinated
