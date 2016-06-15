const _ = require('lodash');
const Promise = require('bluebird');
const fs = Promise.promisifyAll(require('fs'));

const file_name = process.env.FILE || '';
const year = process.env.YEAR || null;
const month = process.env.MONTH || null;


if(_.trim(file_name).length>3 && year && month){
	fs.readFileAsync(file_name+'.json').then(data=>{
		rows = JSON.parse(data);
		states_r = _.map(rows, 'UF');
		states = _.uniq(states_r);
		rows_new = [];
		_.forEach(states, state=>{
			var item = {
				UF: state,
				Ano: parseInt(year),
				Mes: parseInt(month),
				Total: 0,
				Dados: []
			};
			entries_m = _.map(_.filter(rows,{UF: state, SexoConsumidor: 'M'}), entry=>{return _.pick(entry,['FaixaEtariaConsumidor','Quantidade'])});
			entries_f = _.map(_.filter(rows,{UF: state, SexoConsumidor: 'F'}), entry=>{return _.pick(entry,['FaixaEtariaConsumidor','Quantidade'])});
			entries_n = _.map(_.filter(rows,{UF: state, SexoConsumidor: 'N'}), entry=>{return _.pick(entry,['FaixaEtariaConsumidor','Quantidade'])});
			entries_m_reduced = _.reduce(entries_m,(sum,e)=>{return sum + e.Quantidade},0);
			entries_f_reduced = _.reduce(entries_f,(sum,e)=>{return sum + e.Quantidade},0);
			entries_n_reduced = _.reduce(entries_n,(sum,e)=>{return sum + e.Quantidade},0);
			item.Dados.push({
				SexoConsumidor: 'M',
				Total: entries_m_reduced,
				Entradas: entries_m
			});
			item.Dados.push({
				SexoConsumidor: 'F',
				Total: entries_f_reduced,
				Entradas: entries_f
			});
			item.Dados.push({
				SexoConsumidor: 'N',
				Total: entries_n_reduced,
				Entradas: entries_n
			});
			item.Total = entries_m_reduced + entries_f_reduced + entries_n_reduced;
			rows_new.push(item);
		});

		fs.writeFileAsync(file_name+'_formatted.json', JSON.stringify(rows_new)).then(()=>{
			console.log('File formatted');
		});
		
	});
}


